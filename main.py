import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
bot_token = os.getenv("bot_token")
bot_chatID = os.getenv("bot_chatID")    
api_key = os.getenv("api")

# Create dictionaries for each coin
BTC = {"name": "BTC"}
ETH = {"name": "ETH"}
XRP = {"name": "XRP"}
LTC = {"name": "LTC"}
LINK = {"name": "LINK"}

url = "https://api.taapi.io/bulk"

def send_telegram_notification(message):
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + message
    response = requests.get(send_text)
    return response.json()

# def output(message, coin):
    # print(f"This is {coin} \n  RSI: {message[0]['result']['value']}\n  PPO: {message[1]['result']['value']}\n  CCI: {message[2]['result']['value']}")

def checker(coin_dict):
    coin = coin_dict["name"]
    payload = {
        "secret": api_key,
        "construct": {
            "exchange": "gateio",
            "symbol": coin+"/USDT",
            "interval": "1h",
            "indicators": [
                {"indicator": "rsi"}, 
                {"indicator": "ppo"},
                {"indicator": "cci"}
            ]
        }
    }
    headers = {"Content-Type": "application/json"}

    # Send POST request to the API
    response = requests.request("POST", url, json=payload, headers=headers)
    response = response.json()

    response_string = json.dumps(response, indent=4)

    # Extract and format the indicator values
    coin_dict["rsi"] = float(f'{response["data"][0]["result"]["value"]:.2f}')
    coin_dict["ppo"] = float(f'{response["data"][1]["result"]["value"]:.2f}')
    coin_dict["cci"] = float(f'{response["data"][2]["result"]["value"]:.2f}')

    # output(response['data'], coin)

# Check indicators for each coin
coins = [BTC, ETH, XRP, LTC, LINK]
for coin_dict in coins:
    checker(coin_dict)

print(BTC)


#send_telegram_notification(f"Value has exceeded the threshold: {response['data'][0]['result'], response['data'][1]['result']}")

### K is what you want, D is moving average of last 3 intervals. Might be used but 