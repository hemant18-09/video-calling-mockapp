from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from zego_token import generate_token04

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REPLACE THESE WITH YOUR ZEGO CLOUD CREDENTIALS
APP_ID = 1481566233
SERVER_SECRET = "fbda77fa6dd5cc2b978c9df7738a861a"

@app.get("/token")
def get_token(userID: str, roomID: str):
    try:
        # payload = {"room_id": roomID, "privilege": {"1": 1, "2": 1}}
        token_info = generate_token04(APP_ID, SERVER_SECRET, userID, 3600, "")
        return {"token": token_info.token, "appID": APP_ID}
        # return {"token": "implement_token_generation_logic", "appID": APP_ID}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "Zego Token Server is Running"}
