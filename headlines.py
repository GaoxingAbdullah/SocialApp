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

@app.route('/')
def get_news():
    query = request.args.get('publication')
    if not query or query.lower() not in RSS_FEEDS:
        publication = 'bbc'
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    weather = get_weather('Jinhua, China')
    return render_template('home.html', articles=feed['entries'], weather=weather)

def get_weather(query):
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=f3f19918c10bb785e0007af1d0525d08'

    query = urllib.parse.quote(query)
    url = api_url.format(query)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {'description': 
                    parsed['weather'][0]['description'],
                    'temperature':parsed['main']['temp'],
                    'city':parsed['name']
                }
    return weather

if __name__ == '__main__':
    app.run(debug=True)