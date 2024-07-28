from dotenv import load_dotenv
load_dotenv()

import mongo.mongo_utils
from flask import Flask

from news_utils import get_latest_news, save_latest_news, translate_articles

#app = Flask(__name__)


#@app.route('/')
#def hello_world():  # put application's code here
#    return 'Hello World!'


if __name__ == '__main__':
    print("Hello world")
    #latest_news = get_latest_news()
    #save_latest_news(latest_news)
    #translate_articles()
    # app.run()
