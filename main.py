import requests
from twilio.rest import Client


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
alphavantage_api_key = "secretkey"
NEWS_API = "secretkey"
API_TWILIO_KEY = "secretkey"
account_sid = "secretkey"
auth_token = "secretkey"

my_phone = "secretkey"

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"

#------------------- STOCKS API SETUP -----------------#
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": alphavantage_api_key,
}

response_stock = requests.get(STOCK_ENDPOINT, params=stock_params)
response_stock.raise_for_status()
stock_data = response_stock.json()["Time Series (Daily)"]

stock_data_list = [value for (key,value) in stock_data.items()]

today = stock_data_list[0]
yesterday = stock_data_list[1]
day_before_yesterday = stock_data_list[2]

today_closing_price = float(stock_data_list[0]["4. close"])
yesterday_closing_price = float(stock_data_list[1]["4. close"])
day_before_yesterday_closing_price = float(stock_data_list[2]["4. close"])

# ----------------------- If there was a growth of 10% btw yesterday and the day before yesterday ---------------------#

differences = (today_closing_price - yesterday_closing_price)
differences_percent = round((differences / day_before_yesterday_closing_price) * 100)

up_down = None
if differences > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

#---------------- NEWS API SETUP -----------------#
news_parameters = {
    "apiKey": NEWS_API,
    "qInTitle": COMPANY_NAME
}

response_news = requests.get(NEWS_ENDPOINT,params=news_parameters).json()
articles = response_news["articles"]
three_articles = articles[:3]
formatted_articles_list = [[f"{STOCK}: {up_down}{differences_percent}%\nHeadline: {article['title']}.\nBrief: {article['description']}" for article in three_articles]]

# # ----------------------- SEND SMS WITH ARTICLES ---------------------#
up_down = None
if differences > 0:
    up_down = "🔺"
else:
    up_down = "🔻"


for article in formatted_articles_list:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=f"{article}",
        from_=my_phone,
        to='some phone number'
    )

    print(message.status)







