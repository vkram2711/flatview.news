import os
import uuid
from datetime import datetime, timedelta

import langdetect
import requests

from mongo.models import Source, OriginalArticle, TranslatedArticle

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
NEWS_SCRAPPER_API_KEY = os.environ.get('NEWS_SCRAPPER_API_KEY')


exclude_countries = [
    'ru'
]


def yesterday_date():
    today = datetime.now()
    # 24 hours ago
    yesterday = today - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')


# def get_latest_news(page=None):
#     excluded_countries = ','.join([f'!{country}' for country in exclude_countries])
#     url = f'https://newsdata.io/api/1/latest?apikey={NEWS_API_KEY}&prioritydomain=top&image=1&removeduplicate=1'

#     if page is not None:
#         url += f'&page={page}'
#     print(url)

#     # url = f'https://api.worldnewsapi.com/top-news?api-key={NEWS_API_KEY}&source-country={country}&language={language}'
#     return requests.get(url)
def get_latest_news():
    excluded_countries = ','.join([f'!{country}' for country in exclude_countries])
    url = f'https://gnews.io/api/v4/top-headlines?category=general&apikey={NEWS_API_KEY}'
    print(url)
    return requests.get(url)


def get_full_content(url):
    url = f'https://api.worldnewsapi.com/extract-news?api-key={NEWS_SCRAPPER_API_KEY}&url={url}'
    return requests.get(url)

def save_latest_news(latest_news):
    if latest_news.status_code == 200:
        data = latest_news.json()

        # Save data to the mongo db
        #articles = data['top_news'][0]['news']
        #articles = data['results']
        articles = data['articles']
        #next_page = data['nextPage']
        #print('NEXT PAGE:', )
        for article_data in articles:
            print(article_data)

            try:
                #source = Source(
                #    url=article_data.get('url'),
                #    name=article_data.get('source_name', None),
                #    icon=article_data.get('source_icon', None),
                #    creator=article_data.get('author', None)
                #)
                #if article_data.get('creator', None):
                #    creator = article_data.get('creator')[0]
                #else:
                #    creator = None

                if article_data.get('country', None):
                    country = article_data.get('country')[0]
                else:
                    country = None
                url = article_data.get('url')
                source_data = article_data['source']
                source = Source(
                    url=url,
                    name=source_data.get('name', None),
                    #icon=article_data.get('source_icon', None),
                    #creator=creator
                )
                source.save()

                full_content = get_full_content(url)
                content = article_data.get('content', '')

                if full_content.status_code == 200:
                    full_content_data = full_content.json()
                    full_content = full_content_data.get('text', None)
                    if len(full_content) > len(content):
                        content = full_content
                description = article_data.get('description', None)
                article = OriginalArticle(
                    id=str(uuid.uuid4()),
                    language=langdetect.detect(description), #article_data.get('language', 'en'),
                    title=article_data.get('title'),
                    content=content,
                    description=description,
                    #image_url=article_data.get('image_url', None),
                    image_url=article_data.get('image', None),
                    source=source,
                    #publish_date=article_data.get('pubDate'),
                    publish_date=article_data.get('publishedAt'),
                    country=country
                )
                article.save()


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
            except Exception as e:
                print(f'Failed to save article: {article_data} \n\n Error: {e}')
    else:
        print(f'Failed to fetch latest news:{latest_news.status_code}')


def get_last_24_hours_articles():
    today = datetime.now()
    # 24 hours ago
    yesterday = today - timedelta(days=1)
    return OriginalArticle.objects(publish_date__gte=yesterday.strftime('%Y-%m-%d %H:%M:%S')).all()


def get_empty_translations():
    return OriginalArticle.objects(translations__size=0).all()

def get_last_24_hours_articles_as_list():
    articles = get_last_24_hours_articles()
    articles_list = [article.to_mongo().to_dict() for article in articles]
    return articles_list
