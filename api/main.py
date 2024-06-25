"""Main app handler"""

import logging
from os import environ

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.utils.send_messages import send_messages
from api import __version__
import json 
from api.utils.connection import get_mongodb_collection  
from api.utils.message_handler import process_messages
from collections import Counter

logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

DESCRIPTION = """
FASTAPI
"""

root_path: str = environ.get("ROOT_PATH", "")

app = FastAPI(
    root_path=root_path,
    version=__version__,
    description=DESCRIPTION,
    title="FASTAPI",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/send_messages")
async def send_messages_queue(msg_count: int = 10):
    try:
        messages = send_messages(msg_count)
        return messages
    except Exception as e:
        print(f"Failed to send messages: {str(e)}")
        return []


@app.get("/status_counts")
async def get_status_counts(start_time: float = None, end_time: float = None):
    status_count = []
    try:
        collection = get_mongodb_collection()
        cursor = collection.find({})

        messages = list(cursor)
        for msg in messages:
            time = json.loads(msg.get("message")).get("timestamp")
            
            if start_time and end_time:
                if start_time <= time <= end_time:
                    status_count.append(json.loads(msg.get("message")).get("status"))

        counts = Counter(status_count)

        return counts
    except Exception as e:
        print(f"Failed to fetch messages: {str(e)}")
        return []