db.getCollection('users').find({}).forEach(function(value) {
       var sorted = value.photos.sort(function(a,b) {
           return b.likes.summary.total_count - a.likes.summary.total_count
       });
       db.users.update({_id:value.id},{$set: {photos:sorted}})
})
    