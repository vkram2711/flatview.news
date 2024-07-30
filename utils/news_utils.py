import os
import uuid
from datetime import datetime, timedelta

import requests

from mongo.models import Source, OriginalArticle, TranslatedArticle

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

exclude_countries = [
    'ru'
]


def yesterday_date():
    today = datetime.now()
    # 24 hours ago
    yesterday = today - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')


def get_latest_news(country='us', language='en', date=yesterday_date()):
    excluded_countries = ','.join([f'!{country}' for country in exclude_countries])
    url = f'https://newsdata.io/api/1/latest?apikey={NEWS_API_KEY}'
    print(url)

    # url = f'https://api.worldnewsapi.com/top-news?api-key={NEWS_API_KEY}&source-country={country}&language={language}'
    return requests.get(url)


def save_latest_news(latest_news):
    if latest_news.status_code == 200:
        data = latest_news.json()

        # Save data to the mongo db
        #articles = data['top_news'][0]['news']
        articles = data['results']
        for article_data in articles:
            print(article_data)

            try:
                #source = Source(
                #    url=article_data.get('url'),
                #    name=article_data.get('source_name', None),
                #    icon=article_data.get('source_icon', None),
                #    creator=article_data.get('author', None)
                #)
                if article_data.get('creator', None):
                    creator = article_data.get('creator')[0]
                else:
                    creator = None

                if article_data.get('country', None):
                    country = article_data.get('country')[0]
                else:
                    country = None

                source = Source(
                    url=article_data.get('link'),
                    name=article_data.get('source_id', None),
                    icon=article_data.get('source_icon', None),
                    creator=creator
                )
                source.save()

                article = OriginalArticle(
                    id=article_data.get('article_id'),
                    language=article_data.get('language', 'en'),
                    title=article_data.get('title'),
                    content=article_data.get('content'),
                    description=article_data.get('description', None),
                    image_url=article_data.get('image_url', None),
                    source=source,
                    publish_date=article_data.get('pubDate'),
                    country=country
                )

                #article = OriginalArticle(
                #    id=str(article_data.get('id')),
                #    language=article_data.get('language', 'en'),
                #    title=article_data.get('title'),
                #    content=article_data.get('text'),
                #    description=article_data.get('summary', None),
                #    image_url=article_data.get('image', None),
                #    source=source,
                #    publish_date=article_data.get('publish_date')
                #)
                article.save()
            except Exception as e:
                print(f'Failed to save article: {article_data} \n\n Error: {e}')
    else:
        print(f'Failed to fetch latest news:{latest_news.status_code}')


def get_last_24_hours_articles():
    today = datetime.now()
    # 24 hours ago
    yesterday = today - timedelta(days=1)
    return OriginalArticle.objects(publish_date__gte=yesterday.strftime('%Y-%m-%d %H:%M:%S')).all()


def get_last_24_hours_articles_as_list():
    articles = get_last_24_hours_articles()
    articles_list = [article.to_mongo().to_dict() for article in articles]
    return articles_list
