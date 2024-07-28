import asyncio
import json
import os
import time
import uuid
from json import JSONDecodeError

import openai
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from mongo.models import OriginalArticle, TranslatedArticle

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI LLM
llm = ChatOpenAI(model="gpt-4o-mini")

LANGUAGES = [
    #('ar', "Arabic"),
    #('zh-cn', "Chinese (Simplified)"),
    #('en', "English"),
    #('fr', "French"),
    #('de', "German"),
    #('it', "Italian"),
    #('ja', "Japanese"),
    #('ko', "Korean"),
    #('pt', "Portuguese"),
    #('es', "Spanish"),
    ('tr', "Turkish"),
    ('vi', "Vietnamese"),
    ('uk', "Ukrainian")
]


async def translate_articles_to_languages(articles):
    tasks = []
    for article in articles:
        tasks.append(translate_to_languages(article))

    translated_articles = await asyncio.gather(*tasks)
    for i in range(len(translated_articles)):
        original_article = articles[i]

        translation_dict = parse_translations(translated_articles[i])
        translations = []

        for lang, (title, description, content) in translation_dict.items():
            translated_article_model = TranslatedArticle(
                id=uuid.uuid4(),
                original_article=original_article,
                language=lang,
                title=title,
                description=description,
                content=content
            )
            translated_article_model.save()
            translations.append(translated_article_model)
        original_article.translations = translations
        original_article.save()


async def translate_to_languages(article):
    tasks = []
    for lang, full_lang in LANGUAGES:
        if article.language != lang:
            tasks.append(translate_text(article.content, article.title, article.description, full_lang))

    translations = (await llm.agenerate(tasks)).generations
    return dict(zip([lang for lang, _ in LANGUAGES], [translation[0].text for translation in translations]))

# def detect_language(article_content):
#    # Initialize the translator
#    translator = Translator()
#
#    # Detect the language of the article content
#    detected = translator.detect(article_content)
#
#    # Return the detected language
#    return detected.lang


# def translate_text(text, destination):
#    # Initialize the translator
#    translator = Translator()
#    print(f"Original: {text}")

#    # Translate the text
#    translated = translator.translate(text, dest=destination)

#    # Print the original and translated text
#    print(f"Translated: {translated.text}")
#    return translated.text


def translate_text(text, title, description, destination):
    system_prompt = """
    Translate the article's title, description, and full content to the specified language. Ensure that the translation is accurate, professional, and has no grammar or orthographic mistakes. Format the output as JSON in the next format:

    {{"title": "[Translated Title]", "description": "[Translated Description]", "content": "[Translated Full Content]" }}
    """
    description_prompt = "None, generate description and include into output JSON" if description is None else description

    user_prompt = """
    Language: {language}
    Title: {title}
    Description: {description}
    Full Content: {content}
    """
    chat_template = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("user", user_prompt),
        ]
    )

    messages = chat_template.format_messages(language=destination, title=title, description=description_prompt, content=text)

    return messages


async def main():
    article1 = OriginalArticle.objects.filter(id='252771742').first()
    article2 = OriginalArticle.objects.filter(id='252775574').first()
    articles = [article1, article2]
    start_time = time.time()
    await translate_articles_to_languages(articles)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Translation took {elapsed_time:.2f} seconds")


def parse_translations(translations):
    translated_articles = {}
    for lang, translation in translations.items():
        title, description, content = parse_translation(translation)
        translated_articles[lang] = (title, description, content)
    return translated_articles


def parse_translation(json_string):
    if json_string.startswith("```json ") and json_string.endswith(" ```"):
        json_string = json_string[len("```json "):-len(" ```")]
    json_string = json_string.strip()
    try:
        data = json.loads(json_string)
        title = data.get("title", "")
        description = data.get("description", "")
        content = data.get("content", "")
        return title, description, content
    except JSONDecodeError as e:
        print("Failed to parse JSON:", json_string, f"with error: {e}")
        return None, None, None


asyncio.run(main())
