import random
import resend
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

# Load environment variables from the main .env file
load_dotenv()

# Initialize Resend with API key
resend.api_key = os.getenv('RESEND_API_KEY')
from_email = os.getenv('FROM_EMAIL', 'onboarding@resend.dev')  # Default to Resend's test domain

def generate_otp() -> str:
    return str(random.randint(100000, 999999))

def send_otp_email(to_email: str, otp: str):
    try:
        params = {
            "from": from_email,
            "to": [to_email],
            "subject": "Your OTP Verification Code - Sufi Pulse",
            "template": {
                "id": "login-verification-code",
                "variables": {
                    "OTP_CODE": otp
                }
            }
        }

        email = resend.Emails.send(params)
        print(f"Email sent successfully with ID: {email['id']}")
        return email
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        # Fallback to direct HTML if template fails
        html_content = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
            <div style="max-width: 500px; margin: auto; background: #ffffff; border-radius: 12px;
                        padding: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
              <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="color: #065f46; margin: 0;">Sufi Pulse</h2>
                <p style="color: #555; margin: 5px 0;">Your trusted spiritual companion</p>
              </div>

              <p style="color: #333; font-size: 15px;">
                Dear User,<br><br>
                Please use the following One-Time Password (OTP) to complete your verification:
              </p>

              <div style="text-align: center; margin: 25px 0;">
                <span style="display: inline-block; background: #065f46; color: #ffffff;
                             font-size: 24px; font-weight: bold; letter-spacing: 3px;
                             padding: 12px 20px; border-radius: 8px;">
                  {otp}
                </span>
              </div>

              <p style="color: #555; font-size: 14px;">
                This OTP will expire in <b>5 minutes</b>. Please do not share it with anyone.
              </p>

              <p style="color: #999; font-size: 12px; margin-top: 30px; text-align: center;">
                © {datetime.now().year} Sufi Pulse. All rights reserved.
              </p>
            </div>
          </body>
        </html>
        """

        fallback_params = {
            "from": from_email,
            "to": [to_email],
            "subject": "Your OTP Verification Code - Sufi Pulse",
            "html": html_content,
            "text": f"Your OTP is: {otp}. It expires in 5 minutes."
        }

        email = resend.Emails.send(fallback_params)
        print(f"Fallback email sent successfully with ID: {email['id']}")
        return email

def get_otp_expiry() -> datetime:
    return datetime.now(timezone.utc) + timedelta(minutes=5)

def send_template_email(to_email: str, template_id: str, subject: str, variables: dict = None):
    """
    Generic function to send emails using Resend templates
    :param to_email: Recipient's email address
    :param template_id: ID of the template in Resend
    :param subject: Subject of the email
    :param variables: Dictionary of variables to pass to the template (optional)
    :return: Response from Resend API
    """
    try:
        params = {
            "from": from_email,
            "to": [to_email],
            "subject": subject
        }

        if variables:
            params["template"] = {
                "id": template_id,
                "variables": variables
            }
        else:
            params["template"] = {
                "id": template_id
            }

        email = resend.Emails.send(params)
        print(f"Template email sent successfully with ID: {email['id']}")
        return email
    except Exception as e:
        print(f"Error sending template email: {str(e)}")
        # Fallback to a simple HTML email if template fails
        html_content = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
            <div style="max-width: 500px; margin: auto; background: #ffffff; border-radius: 12px;
                        padding: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
              <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="color: #065f46; margin: 0;">Sufi Pulse</h2>
                <p style="color: #555; margin: 5px 0;">Your trusted spiritual companion</p>
              </div>

              <p style="color: #333; font-size: 15px;">
                Dear User,<br><br>
                {subject}: This is a notification from Sufi Pulse.
              </p>

              <p style="color: #555; font-size: 14px;">
                Thank you for using our platform.
              </p>

              <p style="color: #999; font-size: 12px; margin-top: 30px; text-align: center;">
                © {datetime.now().year} Sufi Pulse. All rights reserved.
              </p>
            </div>
          </body>
        </html>
        """

        fallback_params = {
            "from": from_email,
            "to": [to_email],
            "subject": subject,
            "html": html_content,
            "text": f"Sufi Pulse Notification: {subject}"
        }

        email = resend.Emails.send(fallback_params)
        print(f"Fallback template email sent successfully with ID: {email['id']}")
        return email

def send_collaboration_proposal_email(to_email: str):
    """Send collaboration proposal received email"""
    return send_template_email(
        to_email=to_email,
        template_id="collaboration-proposal-received-1",
        subject="Collaboration Proposal Received"
    )

def send_recording_session_confirmation_email(to_email: str):
    """Send recording session confirmation email"""
    return send_template_email(
        to_email=to_email,
        template_id="recording-session-confirmation",
        subject="Recording Session Confirmation"
    )

def send_welcome_email(to_email: str):
    """Send account welcome email"""
    return send_template_email(
        to_email=to_email,
        template_id="account-welcome",
        subject="Welcome to Sufi Pulse"
    )

def send_studio_visit_request_email(to_email: str):
    """Send studio visit request confirmation email"""
    return send_template_email(
        to_email=to_email,
        template_id="studio-visit-request-confirmation",
        subject="Studio Visit Request Submitted"
    )

