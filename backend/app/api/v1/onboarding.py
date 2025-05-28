import pyotp
import base64
from io import BytesIO
import qrcode
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.onboarding import (
    MFASetupRequest, BackupCodeRequest, ProfileSetupRequest,
    PlanSelectionRequest, SyncSetupRequest, TourProgressRequest,
    MFAVerifyRequest, MFAVerifyResponse, BackupCodeVerifyRequest,
    BackupCodeVerifyResponse, ProfileSetupRequest, PlanSelectionRequest
)
from app.models.plan import Plan 
from app.api.deps import get_current_user
from app.models.user import User
from app.core.db import get_db

router = APIRouter()

@router.post("/mfa/setup", response_model=MFASetupResponse)
async def setup_mfa(
    data: MFASetupRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not current_user.mfa_secret:
        secret = pyotp.random_base32()
        current_user.mfa_secret = secret
        current_user.mfa_backup_codes = generate_backup_codes()
        db.add(current_user)
        await db.commit()
        await db.refresh(current_user)
    else:
        secret = current_user.mfa_secret

    totp = pyotp.TOTP(secret)
    otp_uri = totp.provisioning_uri(name=current_user.email, issuer_name="Stratos Cloud")

    qr = qrcode.make(otp_uri)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

    return MFASetupResponse(otp_uri=otp_uri, qr_code_base64=qr_code_base64)


def generate_backup_codes(n=10):
    import secrets
    return [secrets.token_hex(4) for _ in range(n)]

@router.post("/mfa/backup-codes", response_model=BackupCodeResponse)
async def generate_backup_codes(
    data: BackupCodeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    codes = generate_backup_codes()
    current_user.mfa_backup_codes = codes
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return BackupCodeResponse(backup_codes=codes)

@router.post("/mfa/verify", response_model=MFAVerifyResponse)
async def verify_mfa_token(
    data: MFAVerifyRequest,
    current_user: User = Depends(get_current_user),
):
    if not current_user.mfa_secret:
        raise HTTPException(status_code=400, detail="MFA not setup for user")

    totp = pyotp.TOTP(current_user.mfa_secret)
    verified = totp.verify(data.token, valid_window=1)  # allow 1 interval skew

    if not verified:
        raise HTTPException(status_code=401, detail="Invalid MFA token")

    return MFAVerifyResponse(verified=True)

@router.post("/mfa/verify-backup-code", response_model=BackupCodeVerifyResponse)
async def verify_backup_code(
    data: BackupCodeVerifyRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    codes = current_user.mfa_backup_codes or []
    if data.code not in codes:
        raise HTTPException(status_code=401, detail="Invalid backup code")

    # Remove used code
    codes.remove(data.code)
    current_user.mfa_backup_codes = codes
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return BackupCodeVerifyResponse(verified=True)

@router.post("/profile")
async def set_user_profile(
    data: ProfileSetupRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Update user fields if provided
    updated = False

    if data.display_name is not None:
        current_user.display_name = data.display_name
        updated = True
    if data.email is not None:
        # Optionally, verify new email, check duplicates, etc.
        current_user.email = data.email
        updated = True
    if data.bio is not None:
        current_user.bio = data.bio
        updated = True

    if not updated:
        raise HTTPException(status_code=400, detail="No valid fields provided for update")

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return {"message": "User profile updated"}

@router.post("/plan")
async def choose_plan(
    data: PlanSelectionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Plan).filter_by(id=data.plan_id))
    plan = result.scalars().first()
    if not plan:
        raise HTTPException(status_code=400, detail="Invalid plan selected")

    current_user.plan = plan
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return {"message": f"Plan '{plan.name}' selected"}

@router.post("/sync-setup")
async def setup_sync(
    data: SyncSetupRequest,
    current_user: User = Depends(get_current_user)
):
    return {"message": "Sync preferences configured"}

@router.post("/tour/progress")
async def save_tour_progress(
    data: TourProgressRequest,
    current_user: User = Depends(get_current_user)
):
    return {"message": "Tour progress saved"}
