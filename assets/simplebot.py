import os
import requests
import json
import logging
from utils import scrape_webpage, event_exists, store_event, generate_event_hash

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

TOKEN = os.environ.get('BOT_TOKEN')
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    url = BASE_URL + "/sendMessage"
    data = {"text": text.encode("utf8"),
            "chat_id": chat_id,
            "parse_mode": "html"}
    requests.post(url, data)

def lambda_handler(event, context):
    try:
        data = json.loads(event["body"])
        logger.info(data)

        # Preprocess the message
        if 'channel_post' in data.keys():
            message = str(data["channel_post"]["text"])
            chat_id = data["channel_post"]["chat"]["id"]
            first_name = "Unknown"
        else:
            message = str(data["message"]["text"])
            chat_id = data["message"]["chat"]["id"]
            first_name = data["message"]["chat"].get("first_name", "Unknown")

        # Respond to the message based on the command
        if message == "/start":
            response = f"Hello {first_name}"
            logger.info(response)
        
        elif message == "/scrape":
            counter = 0
            response = scrape_webpage()
            for result in response:
                event_hash = generate_event_hash(result)
                if not result.done and not event_exists(event_hash):
                    counter += 1
                    send_message(chat_id, str(result))
                    store_event(event_hash)
                    logger.info(f"Stored {result.title}")

            logger.info(f"Sent {counter} events!")

        elif message == "/scrape all":
            response = scrape_webpage()
            for result in response:
                send_message(chat_id, str(result))
            response = f"Sent {len(response)} events!"
            send_message(chat_id, response)
            logger.info(response)
        
        elif message == "/info":
            response = f"Your Chat ID is {chat_id}"
            send_message(chat_id, response)
            logger.info(response)
        
        else:
            response = "Please use /start or /scrape"
            send_message(chat_id, response)
            logger.info(response)


    except Exception as e:
        print(e)

    # Return a success response
    return {
        'statusCode': 200,
        'body': 'Message sent'
    }
