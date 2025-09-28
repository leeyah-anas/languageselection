import smtplib
from email.message import EmailMessage
from app.core.config import settings

def send_verification_email(email: str, token: str):
    try:
        msg = EmailMessage()
        msg["Subject"] = "Verify your email address - The Roots"
        msg["From"] = "noreply@theroots.com"
        msg["To"] = email
        verification_link = f"http://localhost:8000/api/v1/auth/verify?token={token}"

        # Plain text version
        text_content = f"""
Hello,

Thank you for registering with The Roots!
Please verify your email address by clicking the link below:
{verification_link}

If you did not sign up, please ignore this email.

Best regards,
The Roots Team
"""

        # HTML version
        html_content = f"""
<html>
  <body style='font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;'>
    <div style='max-width: 500px; margin: auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #eee; padding: 30px;'>
      <h2 style='color: #2d7a2d;'>Welcome to The Roots!</h2>
      <p>Thank you for registering. Please verify your email address by clicking the button below:</p>
      <a href='{verification_link}' style='display: inline-block; padding: 12px 24px; background: #2d7a2d; color: #fff; border-radius: 5px; text-decoration: none; font-weight: bold;'>Verify Email</a>
      <p style='margin-top: 20px;'>Or copy and paste this link into your browser:<br><a href='{verification_link}'>{verification_link}</a></p>
      <p style='color: #888; font-size: 12px; margin-top: 30px;'>If you did not sign up for The Roots, you can safely ignore this email.</p>
      <p style='margin-top: 20px;'>Best regards,<br>The Roots Team</p>
    </div>
  </body>
</html>
"""

        msg.set_content(text_content)
        msg.add_alternative(html_content, subtype="html")

        with smtplib.SMTP(settings.MAILTRAP_HOST, settings.MAILTRAP_PORT) as server:
            server.starttls()
            server.login(settings.MAILTRAP_USER, settings.MAILTRAP_PASS)
            server.send_message(msg)
        print(f"✅ Verification email sent to {email}")
    except Exception as e:
        print(f"⚠️ Email sending failed: {e}")
        print(f"📧 Verification link: {verification_link}")
        print("💡 Set up Mailtrap credentials in .env file to enable email sending")
