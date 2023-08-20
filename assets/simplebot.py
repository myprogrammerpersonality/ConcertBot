import os
import requests
import json

TOKEN = os.environ.get('BOT_TOKEN')
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


def lambda_handler(event, context):
    try:
        data = json.loads(event["body"])
        message = str(data["message"]["text"])
        chat_id = data["message"]["chat"]["id"]
        first_name = data["message"]["chat"]["first_name"]

        response = "Please /start, {}".format(first_name)

        if "start" in message:
            response = "Hello {}".format(first_name)

        data = {"text": response.encode("utf8"), "chat_id": chat_id}
        url = BASE_URL + "/sendMessage"
        requests.post(url, data)

    except Exception as e:
        print(e)

    # Return a success response
    return {
        'statusCode': 200,
        'body': 'Message sent'
    }
