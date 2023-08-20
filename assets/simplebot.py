import os
import requests
import json
from utils import scrape_webpage

TOKEN = os.environ.get('BOT_TOKEN')
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    url = BASE_URL + "/sendMessage"
    data = {"text": text.encode("utf8"), "chat_id": chat_id}
    requests.post(url, data)

def lambda_handler(event, context):
    try:
        data = json.loads(event["body"])
        message = str(data["message"]["text"])
        chat_id = data["message"]["chat"]["id"]
        first_name = data["message"]["chat"]["first_name"]


        if message == "/start":
            response = "Hello {}".format(first_name)
        elif message == "/scrape":
            response = scrape_webpage()
        else:
            response = "Please use /start or /scrape"

        send_message(chat_id, response)

    except Exception as e:
        print(e)

    # Return a success response
    return {
        'statusCode': 200,
        'body': 'Message sent'
    }
