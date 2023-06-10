import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
bot_token = os.getenv("bot_token")
bot_chatID = os.getenv("bot_chatID")
api_key = os.getenv("api")

def send_telegram_notification(message):
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + message
    response = requests.get(send_text)
    return response.json()

url = "https://api.taapi.io/bulk"

payload = {
    "secret": api_key,
    "construct": {
        "exchange": "binance",
        "symbol": "ETH/USDT",
        "interval": "1h",
        "indicators": [{"indicator": "rsi"}, {
                "indicator": "ppo"
            },]
    }
}
headers = {"Content-Type": "application/json"}

response = requests.request("POST", url, json=payload, headers=headers)
response = response.json()

response_string = json.dumps(response, indent=4)

print(response_string)

#send_telegram_notification(f"Value has exceeded the threshold: {response['data'][0]['result'], response['data'][1]['result']}")

### K is what you want, D is moving average of last 3 intervals. Might be used but 