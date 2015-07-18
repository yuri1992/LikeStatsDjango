

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
    values.forEach(function(obj) {
       sum.total += obj.value.likes.summary.total_count;
       sum[obj.type] += obj.value.likes.summary.total_count;
    });
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