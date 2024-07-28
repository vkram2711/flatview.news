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


@app.route('/top_news')
def top_news():
    def embed_source(article):
        if 'source' in article and article['source']:
            source = Source.objects.get(id=article['source'])
            article['source'] = source.to_mongo().to_dict()
        return article

    original_articles = OriginalArticle.objects.all()
    translated_articles = TranslatedArticle.objects.all()

    original_articles_json = [embed_source(article.to_mongo().to_dict()) for article in original_articles]
    translated_articles_json = [embed_source(article.to_mongo().to_dict()) for article in translated_articles]

    return json.dumps({
        'original_articles': original_articles_json,
        'translated_articles': translated_articles_json
    }, default=str)


if __name__ == '__main__':
    app.run()
