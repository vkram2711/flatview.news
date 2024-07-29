import asyncio

from dotenv import load_dotenv

from mongo.models import TranslatedArticle

load_dotenv()
from mongo.mongo_utils import load_mongo

load_mongo()

if __name__ == "__main__":
    print(len(TranslatedArticle.objects.all()))