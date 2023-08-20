import os
import requests
import json
import logging
from utils import scrape_webpage

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

TOKEN = os.environ.get('BOT_TOKEN')
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    url = BASE_URL + "/sendMessage"
    data = {"text": text.encode("utf8"), "chat_id": chat_id}
    requests.post(url, data)

def lambda_handler(event, context):
    try:
        data = json.loads(event["body"])
        logger.info(data)

        message = str(data["message"]["text"])
        chat_id = data["message"]["chat"]["id"]
        first_name = data["message"]["chat"].get("first_name", "Unknown")


        if message == "/start":
            response = f"Hello {first_name}"
            logger.info(response)
        elif message == "/scrape":
            response = scrape_webpage()
            for result in response:
                send_message(chat_id, str(result))
            response = f"Sent {len(response)} events!"
            logger.info(response)
        elif message == "/info":
            response = f"Your Chat ID is {chat_id}"
            logger.info(response)
        else:
            response = "Please use /start or /scrape"
            logger.info(response)

        send_message(chat_id, response)

    except Exception as e:
        print(e)

    # Return a success response
    return {
        'statusCode': 200,
        'body': 'Message sent'
    }
