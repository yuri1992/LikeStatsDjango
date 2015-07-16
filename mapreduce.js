var mapFunction = function() {
    obj = {
     'fb_id':this.fb_id,
     'likes':0,
     'photos':this.photos
    }
    emit(this.fb_id,this.photos)
}
var reduce_ = function(key,values) {
    sum = 0
    for (var i in values) {
        sum += values[i]
    }
    return sum
}

db.users.mapReduce(
    mapFunction,
    reduce_,
   {
     out: "session_stat",
   }
)