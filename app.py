import json
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

    start_time = time.time()
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
            '$unwind': {
                'path': '$translations',
                'preserveNullAndEmptyArrays': False
            }
        },
        {
            '$sort': {'publish_date': -1}
        }
    ]

    original_articles = list(OriginalArticle.objects.aggregate(pipeline))

    for article in original_articles:
        translation = article['translations']
        article['title'] = translation['title']
        article['description'] = translation['description']
        article['content'] = translation['content']
        article.pop('translations', None)

    return json.dumps({
        'original_articles': original_articles,
    }, default=str)

if __name__ == '__main__':
    app.run()
