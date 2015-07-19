var mapFunction = function() {
    var self = this;
    this.photos.forEach(function(value) {
        obj = {
            'type':'photos',
            'value':value,
        }
        emit(self.fb_id,obj);
    })
       this.posts.forEach(function(value) {
        obj = {
            'type':'posts',
            'value':value,
        }
        emit(self.fb_id,obj);
    })
    this.videos.forEach(function(value) {
        obj = {
            'type':'videos',
            'value':value,
        }
        emit(self.fb_id,obj);
    })
}
var reduceFunction = function(key,values) {
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
    sum['likers'] = likers;
    return sum;
}
db.users.mapReduce(
    mapFunction,
    reduceFunction,
    {
      //query:{fb_id:'10205447047469248'},
      out:'total_likes'
    }
);