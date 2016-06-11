from havenondemand.hodclient import *
client = HODClient("529be5e4-636a-4a61-9bee-a305f610af00", version="v1")

import json
import os
import time
from flask import Flask, Response, request
import feedparser
import newspaper
from newspaper import Article

app = Flask(__name__, static_url_path='', static_folder='public')
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))


def sentiment(text='I love Haven OnDemand!'):
	params = {'text': text}
	response = client.get_request(params, HODApps.ANALYZE_SENTIMENT, async=False)
	return response['aggregate']['score'],response['aggregate']['sentiment']


def OCR():
	params = {'url': 'http://read.pudn.com/downloads81/sourcecode/math/313101/Unicode%20OCR/Data/Sample%20Images/The%20quick%20brown%20fox%20(Arial)__.jpg'}
	print client.get_request(params, HODApps.OCR_DOCUMENT, async=False)

def requestCompleted(response, error, **kwargs):
  print response

def scraper():
	arr=[]
	url = 'http://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms'
	#url = 'http://rss.cnn.com/rss/edition_technology.rss'
	rss_feed = feedparser.parse(url)
	for post in rss_feed.entries:
	    print post.title
	    a = Article(post.link)
	    a.download()
	    a.parse()
	    score,senti = sentiment(a.text)
	    d={}
	    d['text']=a.text
	    d['url']=post.link
	    d['score']=score
	    d['sentiment']=senti
	    d['title']=post.title
	    arr.append(d)
	
	with open('comments.json', 'w') as f:
	    f.write(json.dumps(arr, indent=4, separators=(',', ': ')))


@app.route('/api', methods=['GET', 'POST'])
def comments_handler():
    with open('news.json', 'r') as f:
        comments = json.loads(f.read())

    if request.method == 'POST':
        new_comment = request.form.to_dict()
        new_comment['id'] = int(time.time() * 1000)
        comments.append(new_comment)

        with open('news.json', 'w') as f:
            f.write(json.dumps(comments, indent=4, separators=(',', ': ')))

    return Response(
        json.dumps(comments),
        mimetype='application/json',
        headers={
            'Cache-Control': 'no-cache',
            'Access-Control-Allow-Origin': '*'
        }
    )


if __name__ == '__main__':
	scraper()	
	#app.run(debug=True,host='0.0.0.0')



