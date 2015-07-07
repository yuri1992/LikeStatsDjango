import mongoengine


class Count(mongoengine.EmbeddedDocument):
    total_count = mongoengine.IntField()


class LikeBase(mongoengine.EmbeddedDocument):
    pic_small = mongoengine.URLField()
    name = mongoengine.StringField()
    can_post = mongoengine.StringField()
    id = mongoengine.IntField()


class Likes(mongoengine.EmbeddedDocument):
    data = mongoengine.ListField()
    summary = mongoengine.EmbeddedDocumentField(Count)
    cursors = mongoengine.StringField()
    paging = mongoengine.StringField()


class Photo(mongoengine.EmbeddedDocument):
    id = mongoengine.IntField()
    picture = mongoengine.URLField()
    name = mongoengine.StringField()
    created_time = mongoengine.StringField()
    #likes = mongoengine.EmbeddedDocumentListField(Likes)
    likes = mongoengine.ListField()


class Video(mongoengine.EmbeddedDocument):
    id = mongoengine.IntField()
    picture = mongoengine.URLField()
    name = mongoengine.StringField()
    created_time = mongoengine.StringField()
    likes = mongoengine.EmbeddedDocumentListField(Likes)


class Post(mongoengine.EmbeddedDocument):
    id = mongoengine.IntField()
    picture = mongoengine.URLField()
    name = mongoengine.StringField()
    created_time = mongoengine.StringField()
    likes = mongoengine.EmbeddedDocumentListField(Likes)


class Users(mongoengine.Document):
    fb_id = mongoengine.IntField()
    email = mongoengine.EmailField()
    birthday = mongoengine.StringField()
    first_name = mongoengine.StringField()
    last_name = mongoengine.StringField()
    gender = mongoengine.StringField()
    link = mongoengine.URLField()
    access_token = mongoengine.StringField()
    access_token_expires = mongoengine.IntField()
    photos = mongoengine.EmbeddedDocumentListField(Photo)
    videos = mongoengine.EmbeddedDocumentListField(Video)
    posts = mongoengine.EmbeddedDocumentListField(Post)
