import os
from dotenv import load_dotenv
load_dotenv()

SMTP_SERVER = 'smtp.sendgrid.net'
SMTP_PORT = 587
SMTP_USERNAME = 'apikey'
# Load the API Key from an environment variable
SMTP_PASSWORD = os.getenv('SENDGRID_API_KEY')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
LANDING_PAGE_URL = 'http://localhost:8000/click' 