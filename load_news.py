import asyncio

from dotenv import load_dotenv

load_dotenv()

from translation_utils import translate_articles_to_languages
from news_utils import get_latest_news, save_latest_news, get_last_24_hours_articles_as_list, get_last_24_hours_articles

from mongo.mongo_utils import load_mongo

load_mongo()


if __name__ == '__main__':
    latest_news = get_latest_news(country='fr', language='fr')
    print(latest_news.json())
    #save_latest_news(latest_news)
    articles = get_last_24_hours_articles()
    short_articles = []
    for i in range(0, 5):
        short_articles.append(articles[i])
    #print(articles)
    asyncio.run(translate_articles_to_languages(short_articles))

