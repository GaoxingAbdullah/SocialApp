from flask import Flask,render_template, request
import feedparser
import json
import urllib
import urllib.parse
import urllib.request



app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
                'cnn': 'http://rss.cnn.com/rss/edition.rss',
                'fox': 'http://feeds.foxnews.com/foxnews/latest',
                'iol': 'http://www.iol.co.za/cmlink/1.640'}

DEFAULTS = { 'publication': 'bbc',
              'city':'London, UK',
              'currency_from':'GBP',
              'currency_to':'USD'}


WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=f3f19918c10bb785e0007af1d0525d08'
CURRENCY_URL = 'https://openexchangerates.org//api/latest.json?app_id=a45f455074364ff1a7d5ed38c2b37403'


@app.route('/')
def home():
    #get customized headlines, based on user input or default
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)  
    #get customized weather, based on user input or default  
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
     #get customized CURRENCY, based on user input or default  
    currency_from = request.args.get('currency_from')
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get('currency_to')
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate = get_rate(currency_from, currency_to)

    return render_template('home.html', articles=articles, weather=weather, 
                            currency_from=currency_from, currency_to=currency_to, rate=rate)


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']

def get_weather(query):
    query = urllib.parse.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {'description': 
                    parsed['weather'][0]['description'],
                    'temperature':parsed['main']['temp'],
                    'city':parsed['name'],
                    'country':parsed['sys']['country']
                }
    return weather

#currency api 
def get_rate(frm, to):
    all_currency = urllib.request.urlopen(CURRENCY_URL).read()

    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())

    return to_rate/frm_rate
    
if __name__ == '__main__':
    app.run(debug=True)