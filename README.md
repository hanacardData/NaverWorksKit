# NaverWorksKit

A simple toolkit to integrate with Naver Works Bot API — so you don’t have to suffer through the official documentation.

## Features
- Easy bot message sending (channel & user)
- Automatic access token management
- Simple FastAPI server to handle webhook events

## Getting Started
1. Clone the repository
```bash
git clone https://github.com/hanacardData/NaverWorksKit.git
cd NaverWorksKit
```

2. Create a .env file in the project root and fill in your credentials:
```
WORKS_CLIENT_ID=your_client_id
WORKS_CLIENT_SECRET=your_client_secret
SERVICE_ACCOUNT=your_service_account
PRIVATE_KEY_PATH=./secret/private.pem
BOT_ID=your_bot_id
```

3. Install dependencies
```python
pip install -r requirements.txt
```

4. Run the FastAPI server with Uvicorn
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001 # dev
uvicorn app.main:app --host 0.0.0.0 --port 8001 --workers 4 # production
```
