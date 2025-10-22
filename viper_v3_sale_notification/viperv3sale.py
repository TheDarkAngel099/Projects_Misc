import time
import argparse
from twilio.rest import Client
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


parser = argparse.ArgumentParser(description="Amazon price tracker with Twilio alerts")
parser.add_argument("--sid", required=True, help="Twilio Account SID")
parser.add_argument("--token", required=True, help="Twilio Auth Token")
parser.add_argument("--twilio", required=True, help="Twilio phone number")
parser.add_argument("--recipients", nargs="+", required=True, help="List of recipient phone numbers")
args = parser.parse_args()


mouse_url = "https://www.amazon.in/Razer-Viper-Wireless-Esports-Gaming/dp/B0CVRGCGWJ"
driver = webdriver.Chrome()
driver.get(mouse_url)
time.sleep(5)


whole = driver.find_element(By.CLASS_NAME, "a-price-whole").text
fraction = driver.find_element(By.CLASS_NAME, "a-price-fraction").text
price_str = whole.replace(",", "") + "." + fraction
price_float = float(price_str)

print("Price as string:", price_str)
print("Price as float:", price_float)

driver.quit()


usual_price = 12999
if price_float < usual_price:
    message_body = f"Razer Viper V3 is on sale! Current price: ₹{price_str} 🥺"
    client = Client(args.sid, args.token)
    for number in args.recipients:
        message = client.messages.create(
            body=message_body,
            from_=args.twilio,
            to=number
        )
        print("SMS sent to", number, ":", message.sid)
