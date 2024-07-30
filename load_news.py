import asyncio
import time

from dotenv import load_dotenv

load_dotenv()

from utils.translation_utils import translate_articles_to_languages
from utils.news_utils import get_latest_news, get_last_24_hours_articles, save_latest_news, get_empty_translations

from mongo.mongo_utils import load_mongo

load_mongo()


def process_in_batches(array, batch_size=5):
    # Loop over the array in steps of batch_size
    for i in range(0, len(array), batch_size):
        # Yield a batch of elements
        yield array[i:i + batch_size]


if __name__ == '__main__':
    #next_page = None
    #for i in range (0, 1):
    #    latest_news = get_latest_news()
    #    print("Fetched latest news")
    #    next_page = save_latest_news(latest_news)
    #    print("Saved latest news")
    articles = get_empty_translations()
    print(articles)
#
    #for batch in process_in_batches(articles):
    #    asyncio.run(translate_articles_to_languages(batch))
    #    print("Translated batch of articles")
    #    time.sleep(60)


    ##print(articles)
    #

