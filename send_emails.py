from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import *

recipients = {
    'Zack': 'zack@xoltar.com'
}

for name, email in recipients.items():
    body = f"""
    Hi {name},<br><br>
    Please review the updated HR policy:<br>
    <a href="{LANDING_PAGE_URL}?user={name}">View Policy</a>
    <br><br>
    Regards,<br>
    HR Team
    """
    
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=email,
        subject='URGENT: HR Policy Update Required',
        html_content=body)
    
    try:
        # The SendGrid API Key is stored in the SMTP_PASSWORD variable in config.py
        sg = SendGridAPIClient(SMTP_PASSWORD)
        response = sg.send(message)
        print(f"Email sent to {name} ({email}). Status code: {response.status_code}")
        if response.status_code >= 400:
            print("Response body:", response.body)
    except Exception as e:
        print(f"Error sending email to {name} ({email}): {e}")

print("\nEmail sending process finished.") 