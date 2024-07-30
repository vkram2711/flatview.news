import json
import os
import time

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
    language = request.args.get('language', 'en')
    pipeline = [
        {
            '$lookup': {
                'from': 'source',
                'localField': 'source',
                'foreignField': '_id',
                'as': 'source'
            }
        },
        {
            '$unwind': {
                'path': '$source',
                'preserveNullAndEmptyArrays': True
            }
        },
        {
            '$lookup': {
                'from': 'translated_article',
                'let': {'article_id': '$_id'},
                'pipeline': [
                    {
                        '$match': {
                            '$expr': {
                                '$and': [
                                    {'$eq': ['$original_article', '$$article_id']},
                                    {'$eq': ['$language', language]}
                                ]
                            }
                        }
                    }
                ],
                'as': 'translations'
            }
        },
        {
            '$addFields': {
                'translations': {
                    '$cond': {
                        'if': {'$eq': ['$language', language]},
                        'then': [],
                        'else': '$translations'
                    }
                }
            }
        },
        {
            '$match': {
                '$or': [
                    {'language': {'$eq': language}},
                    {'translations': {'$ne': []}}
                ]
            }
        },
        {
            '$unwind': {
                'path': '$translations',
                'preserveNullAndEmptyArrays': True
            }
        },
        {
            '$sort': {'publish_date': -1}
        }
    ]

    original_articles = list(OriginalArticle.objects.aggregate(pipeline))

    for article in original_articles:
        if 'translations' in article:
            translation = article['translations']
            article['title'] = translation['title']
            article['description'] = translation['description']
            article.pop('translations', None)
            article.pop('content', None)

    return json.dumps({
        'original_articles': original_articles,
    }, default=str)


@app.route('/article/<article_id>')
def get_article_by_id(article_id):
    language = request.args.get('language', 'en')
    article = OriginalArticle.objects(id=article_id).first()
    if article:
        source = Source.objects(id=article.source.id).first()
        article = article.to_mongo().to_dict()
        article["source"] = source.to_mongo().to_dict()
        if language != article["language"]:
            translation = TranslatedArticle.objects(original_article=article["_id"], language=language).first()
            if translation:
                article["title"] = translation.title
                article["description"] = translation.description
                article["content"] = translation.content
            else:
                article["title"] = "Translation not available"
                article["description"] = "Translation not available"
                article["content"] = "Translation not available"
        return json.dumps(article, default=str)
    else:
        return json.dumps({'error': 'Article not found'}), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
