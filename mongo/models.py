from mongoengine import Document, StringField, ListField, ReferenceField, UUIDField, URLField


class Source(Document):
    url = URLField()
    name = StringField(null=True)
    icon = URLField(null=True)
    creator = StringField(null=True)


class OriginalArticle(Document):
    id = StringField(primary_key=True)
    language = StringField(required=True)

    title = StringField(required=True)
    content = StringField(required=True)
    description = StringField(null=True)

    image_url = URLField(null=True)

    publish_date = StringField()
    source=ReferenceField(Source)
    translations = ListField(ReferenceField('TranslatedArticle'))


class TranslatedArticle(Document):
    id = UUIDField(primary_key=True)
    language = StringField(required=True)

    title = StringField(required=True)
    content = StringField(required=True)
    description = StringField(null=True)

    original_article = ReferenceField(OriginalArticle)


