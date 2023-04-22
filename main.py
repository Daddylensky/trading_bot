import requests
import json
import time
import csv
from datetime import datetime

API_KEY = "3cbea6b5-32b8-492c-8448-d49aa449cbdc"
CRYPTOCURRENCY_ID = 1  # Bitcoin's ID
INTERVAL = 60  # Fetch the data every 60 seconds (1 minute)

def get_latest_price(api_key, cryptocurrency_id):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": api_key,
    }
    params = {
        "id": cryptocurrency_id,
    }
    response = requests.get(url, headers=headers, params=params)
    data = json.loads(response.text)
    return data["data"][str(cryptocurrency_id)]["quote"]["USD"]["price"]

def write_to_csv(timestamp, price):
    with open(r"C:\Users\oboda\Dropbox\PC\Desktop\rich\crypto\historical_data.csv", mode="a", newline='') as csvfile:
        fieldnames = ["timestamp", "price"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header only if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow({"timestamp": timestamp, "price": price})

if __name__ == "__main__":
    while True:
        try:
            price = get_latest_price(API_KEY, CRYPTOCURRENCY_ID)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            write_to_csv(timestamp, price)
            print(f"{timestamp}: {price}")
            time.sleep(INTERVAL)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(INTERVAL)
