import requests
from twilio.rest import Client


STOCK_NAME = "STOCK name"
COMPANY_NAME = "Company name"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
stock_api_key = "Your API ley"

TWILIO_SID = 'Your SID'
TWILIO_TOKEN = 'Your auth token'


    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol" : STOCK_NAME,
    "apikey": stock_api_key,
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
data = response.json()['Time Series (Daily)']


#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

data_list = [value for (key,value) in data.items()]

yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]


#TODO 2. - Get the day before yesterday's closing stock price

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.

diff_percent =   round((difference / float(yesterday_closing_price)) * 100)

#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").

new_api_key = "Your api key"
endpoint = "Your endpoint"

    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

if diff_percent > 1:
    news_param = {
        "apiKey": new_api_key,
        "qInTitle": COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_param)
    articles = news_response.json()["articles"]


#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_Articles = articles[:3]
    print(three_Articles)

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [f"{STOCK_NAME}: {up_down} {diff_percent}% \nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_Articles]

#TODO 9. - Send each article as a separate message via Twilio.
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body= article,
            from_='Twilio number',
            to='Reciever number'
        )
        print(message.status)

