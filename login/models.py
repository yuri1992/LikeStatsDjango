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


class Friend(mongoengine.EmbeddedDocument):
    fb_id = mongoengine.IntField()


class UsersQuerySet(mongoengine.QuerySet):

    def redue_likes(self):
        reduce_obj = self.map_reduce(Code("""
                function() {
                    var self = this;
                    
                    this[~photos].forEach(function(value) {
                        obj = {
                            'type':'photos',
                            'value':value,
                        }
                        emit(self.fb_id,obj);
                    })
                    this[~posts].forEach(function(value) {
                        obj = {
                            'type':'posts',
                            'value':value,
                        }
                        emit(self.fb_id,obj);
                    })
                    this[~videos].forEach(function(value) {
                        obj = {
                            'type':'videos',
                            'value':value,

                        }
                        emit(self.fb_id,obj);
                    })
                }"""),
                Code(""" 
                function(key,values) {
                    sum = {
                        'total':0,
                        'photos':0,
                        'videos':0,
                        'posts':0,
                        'top_likers': [],
                        'top_photos': [],
                        'top_posts': [],
                        'top_videos': [],
                    };   
                    values.forEach(function(obj) {
                       sum.total += obj.value.likes.summary.total_count;
                       sum[obj.type] += obj.value.likes.summary.total_count;
                    });
                    return sum;
                }
                """), 'map_reduce')
        return list(reduce_obj)


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
    friends = mongoengine.EmbeddedDocumentListField(Friend)

    meta = {'queryset_class': UsersQuerySet}


class RequestsLog(mongoengine.DynamicDocument):
    url = mongoengine.StringField()


class Stats(mongoengine.Document):
    total_likes = mongoengine.IntField()
    photos_likes = mongoengine.IntField()
    videos_likes = mongoengine.IntField()
    posts_likes = mongoengine.IntField()
    sorted_photos = mongoengine.EmbeddedDocumentListField(Photo)
    sorted_videos = mongoengine.EmbeddedDocumentListField(Video)
    sorted_posts = mongoengine.EmbeddedDocumentListField(Post)
