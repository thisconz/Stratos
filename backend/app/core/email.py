def send_verification_email(email: str, token: str):
    link = f"http://localhost:3000/verify-email?token={token}"  # frontend handles UI
    print(f"[DEV] Send to {email}: Click to verify: {link}")
