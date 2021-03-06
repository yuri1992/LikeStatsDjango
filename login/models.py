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
    images = mongoengine.ListField()


class Video(mongoengine.EmbeddedDocument):
    id = mongoengine.StringField(name='video_id')
    picture = mongoengine.URLField()
    name = mongoengine.StringField()
    embed_html = mongoengine.StringField()
    description = mongoengine.StringField()
    embeddable = mongoengine.BooleanField()
    created_time = mongoengine.StringField()
    updated_time = mongoengine.StringField()
    likes = mongoengine.DictField()


class Post(mongoengine.EmbeddedDocument):
    id = mongoengine.StringField(name='post_id')
    picture = mongoengine.URLField()
    full_picture = mongoengine.URLField()
    name = mongoengine.StringField()
    description = mongoengine.StringField()
    caption = mongoengine.StringField()
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
                        'fb_id':key,
                        'total':0,
                        'photos':0,
                        'videos':0,
                        'posts':0,
                        'top_likers': [],
                    };
                    total_likers = {};
                    likers = {};
                    
                    values.forEach(function(obj) {
                        if (typeof(obj.value.likes.data) != 'undefined') {
                           obj.value.likes.data.forEach(function(user) {
                               if (typeof total_likers[user.id] == "undefined") {
                                   total_likers[user.id] = 0;
                                   likers[user.id] = user
                               }
                               total_likers[user.id] += 1;
                           })
                           sum.total += obj.value.likes.summary.total_count;
                           sum[obj.type] += obj.value.likes.summary.total_count;
                       }
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
                """), {'merge': 'likes_stats'})
        return list(reduce_obj)

    def sort_elements(self):
        return self.exec_js("""
            db[collection].find(query).forEach(function(value) {
                    if (value[~photos].length > 0) {
                       var sorted = value[~photos].sort(function(a,b) {
                        if (typeof b.likes.summary != 'undefined' && typeof a.likes.summary != 'undefined')
                           return b.likes.summary.total_count - a.likes.summary.total_count
                       });
                       //db[collection].update(query,{$set: {photos:sorted}})
                       db['likes_stats'].update({'value.fb_id':value[~fb_id]},{$set: {'value.sorted_photos':sorted}},{upsert:true})
                    }
                    if (value[~videos].length > 0) {
                       var sorted = value[~videos].sort(function(a,b) {
                        if (typeof b.likes.summary != 'undefined' && typeof a.likes.summary != 'undefined')
                           return b.likes.summary.total_count - a.likes.summary.total_count
                       });
                       //db[collection].update(query,{$set: {videos:sorted}})
                        db['likes_stats'].update({'value.fb_id':value[~fb_id]},{$set: {'value.sorted_videos':sorted}},{upsert:true})

                    }
                    if (value[~posts].length > 0) {
                       var sorted = value[~posts].sort(function(a,b) {
                           if (typeof b.likes.summary != 'undefined' && typeof a.likes.summary != 'undefined')
                                return b.likes.summary.total_count - a.likes.summary.total_count
                       });
                       //db[collection].update(query,{$set: {posts:sorted}})
                       db['likes_stats'].update({'value.fb_id':value[~fb_id]},{$set: {'value.sorted_posts':sorted}},{upsert:true})

                    }
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
    picture = mongoengine.DictField(name='profile_photo')
    cover = mongoengine.DictField(name='cover_photo')
    access_token = mongoengine.StringField()
    access_token_expires = mongoengine.IntField()
    photos = mongoengine.EmbeddedDocumentListField(Photo)
    videos = mongoengine.EmbeddedDocumentListField(Video)
    posts = mongoengine.EmbeddedDocumentListField(Post)
    friends = mongoengine.EmbeddedDocumentListField(Friend)
    last_time_fetch = mongoengine.DateTimeField()
    last_finish_fetch = mongoengine.DateTimeField()
    fetching_status = mongoengine.BooleanField(default=False)

    meta = {'queryset_class': UsersQuerySet}


class Stats(mongoengine.EmbeddedDocument):
    fb_id = mongoengine.IntField()
    total = mongoengine.IntField()
    photos = mongoengine.IntField()
    videos = mongoengine.IntField()
    posts = mongoengine.IntField()
    top_likers = mongoengine.ListField()
    sorted_videos = mongoengine.EmbeddedDocumentListField(Video)
    sorted_posts = mongoengine.EmbeddedDocumentListField(Post)
    sorted_photos = mongoengine.EmbeddedDocumentListField(Photo)


class Likes_Stats(mongoengine.Document):
    value = mongoengine.EmbeddedDocumentField(Stats)
    meta = {
        'collection': 'likes_stats'
    }


class RequestsLog(mongoengine.DynamicDocument):
    url = mongoengine.StringField()
