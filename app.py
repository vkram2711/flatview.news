import json

from dotenv import load_dotenv
load_dotenv()
from flask_cors import CORS

from mongo.models import OriginalArticle, TranslatedArticle, Source
from mongo.mongo_utils import load_mongo

load_mongo()

from flask import Flask


app = Flask(__name__)
CORS(app)


from flask import request


@app.route('/top_news')
def top_news():
    def embed_source(article):
        if 'source' in article and article['source']:
            source = Source.objects.get(id=article['source'])
            article['source'] = source.to_mongo().to_dict()
        return article

    def embed_translations(article, language):
        if article['language'] == language:
            return article

        if 'translations' in article and article['translations']:
            translation = TranslatedArticle.objects(original_article=article['_id'], language=language).first()
            if translation:
                translation = translation.to_mongo().to_dict()
                article['title'] = translation['title']
                article['description'] = translation['description']
                article['content'] = translation['content']
                return article
        return None

    language = request.args.get('language', 'en')
    original_articles = OriginalArticle.objects.order_by('-publish_date').all()

    original_articles_json = [
        embed_translations(embed_source(article.to_mongo().to_dict()), language)
        for article in original_articles
    ]

    # Filter out None values
    original_articles_json = [article for article in original_articles_json if article]

    return json.dumps({
        'original_articles': original_articles_json,
    }, default=str)


if __name__ == '__main__':
    app.run()
