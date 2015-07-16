import mongoengine


class Count(mongoengine.EmbeddedDocument):
    total_count = mongoengine.IntField()


class LikeBase(mongoengine.EmbeddedDocument):
    pic_small = mongoengine.URLField(null=True)
    name = mongoengine.StringField(null=True)
    can_post = mongoengine.BooleanField(null=True)
    id = mongoengine.IntField(null=True)


class Likes(mongoengine.EmbeddedDocument):
    data = mongoengine.EmbeddedDocumentListField(LikeBase)
    summary = mongoengine.EmbeddedDocumentField(Count)
    paging = mongoengine.DictField(null=True)
    cursors = mongoengine.DictField(null=True)

    def __str__(self):
        return "Like Object"


class Photo(mongoengine.EmbeddedDocument):
    id = mongoengine.StringField(name='photo_id')
    picture = mongoengine.StringField()
    name = mongoengine.StringField()
    created_time = mongoengine.StringField()
    #likes = mongoengine.EmbeddedDocumentListField(Likes)
    likes = mongoengine.DictField()


class Video(mongoengine.EmbeddedDocument):
    id = mongoengine.StringField(name='video_id')
    picture = mongoengine.URLField()
    name = mongoengine.StringField()
    created_time = mongoengine.StringField()
    updated_time = mongoengine.StringField()
    likes = mongoengine.DictField()


class Post(mongoengine.EmbeddedDocument):
    id = mongoengine.StringField(name='post_id')
    picture = mongoengine.URLField()
    name = mongoengine.StringField()
    created_time = mongoengine.StringField()
    updated_time = mongoengine.StringField()
    likes = mongoengine.DictField()


class Users(mongoengine.DynamicDocument):

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


class RequestsLog(mongoengine.DynamicDocument):
    url = mongoengine.StringField()
