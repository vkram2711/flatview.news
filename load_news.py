import asyncio
import time

from dotenv import load_dotenv

load_dotenv()

from utils.translation_utils import translate_articles_to_languages
from utils.news_utils import get_latest_news, get_last_24_hours_articles, save_latest_news

from mongo.mongo_utils import load_mongo

load_mongo()


if __name__ == '__main__':
    #latest_news = get_latest_news(country='us', language='en')
    #print(latest_news.json())
    #save_latest_news(latest_news)
    articles = get_last_24_hours_articles()
    short_articles = []
    for i in range(5, 10):
        short_articles.append(articles[i])
    asyncio.run(translate_articles_to_languages(short_articles))
    #time.sleep(60)

    #for i in range(5, 10):
    #    short_articles.append(articles[i])

    #asyncio.run(translate_articles_to_languages(short_articles))
    ##print(articles)
    #

