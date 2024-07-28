import asyncio
import os
import time

import openai
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from mongo.models import OriginalArticle

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI LLM
llm = ChatOpenAI(model="gpt-4o-mini")

LANGUAGES = [
    ('ar', "Arabic"),
    ('zh-cn', "Chinese (Simplified)"),
    ('en', "English"),
    ('fr', "French"),
    ('de', "German"),
    ('it', "Italian"),
    ('ja', "Japanese"),
    ('ko', "Korean"),
    ('pt', "Portuguese"),
    ('es', "Spanish"),
    ('tr', "Turkish"),
    ('vi', "Vietnamese"),
    ('uk', "Ukrainian")
]


async def translate_to_languages(article):
    tasks = []
    for lang, full_lang in LANGUAGES:
        tasks.append(translate_text(article.content, article.title, article.description, full_lang))

    translations = await asyncio.gather(*tasks)
    return dict(zip([lang for lang, _ in LANGUAGES], translations))


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


async def translate_text(text, title, description, destination):
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

    response = await llm.agenerate([messages])
    print(f"Original: {text}")
    print(f"Translated: {response}")

    return response


async def main():
    article = OriginalArticle.objects.filter(id='252771742').first()
    start_time = time.time()
    translations = await translate_to_languages(article)
    print(translations)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Translation took {elapsed_time:.2f} seconds")


asyncio.run(main())
