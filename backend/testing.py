import asyncio

from dotenv import load_dotenv
from langdetect import detect

from mongo.models import TranslatedArticle

load_dotenv()
from mongo.mongo_utils import load_mongo

load_mongo()

if __name__ == "__main__":
    language = detect("Повітряна тривога зараз в Україні 31 липня 2024 року: в яких областях оголошена та чому")
    print(language)
