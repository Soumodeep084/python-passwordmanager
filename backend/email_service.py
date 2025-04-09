import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import MAILTRAP_CONFIG

# Function to send OTP email using mailtrap.io
def send_otp_email(email, subject , body):
    
    # Create the email
    msg = MIMEMultipart()
    msg["From"] = MAILTRAP_CONFIG["sender_email"]
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    # Send the email using Mailtrap.io
    try:
        with smtplib.SMTP(MAILTRAP_CONFIG["smtp_server"], MAILTRAP_CONFIG["smtp_port"]) as server:
            server.login(MAILTRAP_CONFIG["sender_email"], MAILTRAP_CONFIG["sender_password"])
            server.sendmail(MAILTRAP_CONFIG["sender_email"], email, msg.as_string())
    except Exception as e:
        print(f"Failed to send OTP email: {str(e)}")


# Function to send OTP email using orignal email
# def send_otp_email(email, otp):
#     # Email content
#     subject = "OTP for Account Verification - EncryptPass The password Manager"
#     body = f"""
#     <h2>Welcome to EncryptPass!</h2>
#     <p>Thank you for registering with us. Below is your OTP for account verification:</p>
#     <h3>{otp}</h3>
#     <p><strong>Do not share this OTP with anyone.</strong></p>
#     <p>This OTP is valid for 5 minutes.</p>
#     """

#     # Create the email
#     msg = MIMEMultipart()
#     msg["From"] = EMAIL_CONFIG["sender_email"]
#     msg["To"] = email
#     msg["Subject"] = subject
#     msg.attach(MIMEText(body, "html"))

#     # Send the email
#     try:
#         with smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"]) as server:
#             server.starttls()
#             server.login(EMAIL_CONFIG["sender_email"], EMAIL_CONFIG["sender_password"])
#             server.sendmail(EMAIL_CONFIG["sender_email"], email, msg.as_string())
#         print(f"OTP sent to {email}")
#     except Exception as e:
#         print(f"Failed to send OTP email: {str(e)}")