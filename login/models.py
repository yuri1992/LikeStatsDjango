from bson import Code
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
    id = mongoengine.IntField(name='fb_id')
    name = mongoengine.StringField()


class UsersQuerySet(mongoengine.QuerySet):

    def reduce_likes(self):
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
                    };
                    total_likers = {};
                    likers = {};
                    
                    values.forEach(function(obj) {
                       obj.value.likes.data.forEach(function(user) {
                           if (typeof total_likers[user.id] == "undefined") {
                               total_likers[user.id] = 0;
                               likers[user.id] = user
                           }
                           total_likers[user.id] += 1;
                       })
                       sum.total += obj.value.likes.summary.total_count;
                       sum[obj.type] += obj.value.likes.summary.total_count;
                    });
                    for (var i in total_likers) {
                        value = total_likers[i];
                        likers[i]['total_likes'] = value;
                        sum['top_likers'].push(likers[i]);
                    }
                    sum['top_likers'] = sum['top_likers'].sort(function(a,b) { 
                            return b.total_likes - a.total_likes;
                        });
                    return sum;
                }
                """), 'likes_stats')
        return list(reduce_obj)

    def sort_elements(self):
        return self.exec_js("""
            db[collection].find(query).forEach(function(value) {
                   var sorted = value[~photos].sort(function(a,b) {
                       return b.likes.summary.total_count - a.likes.summary.total_count
                   });
                   db[collection].update(query,{$set: {photos:sorted}})

                   var sorted = value[~videos].sort(function(a,b) {
                       return b.likes.summary.total_count - a.likes.summary.total_count
                   });
                   db[collection].update(query,{$set: {videos:sorted}})

                   var sorted = value[~posts].sort(function(a,b) {
                       return b.likes.summary.total_count - a.likes.summary.total_count
                   });
                   db[collection].update(query,{$set: {posts:sorted}})
            })
            return {};
        """)


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


class Stats(mongoengine.Document):
    fb_id = mongoengine.IntField()
    total_likes = mongoengine.IntField()
    photos_likes = mongoengine.IntField()
    videos_likes = mongoengine.IntField()
    posts_likes = mongoengine.IntField()
    sorted_photos = mongoengine.EmbeddedDocumentListField(Photo)
    sorted_videos = mongoengine.EmbeddedDocumentListField(Video)
    sorted_posts = mongoengine.EmbeddedDocumentListField(Post)


class RequestsLog(mongoengine.DynamicDocument):
    url = mongoengine.StringField()
