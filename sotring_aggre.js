/*
db.getCollection('users').aggregate([
    { $match: {
        'fb_id': 10205447047469250
    }},
    // Expand the scores array into a stream of documents
    { $unwind: '$videos' },
    // Sort in descending order
    { $sort: {
        'videos.likes.summary.total_count': -1
    }}
    ],
    {
        explain:true,
        out:'total_likes'
    }
)
*/    
db.getCollection('users').aggregate([
    { $match: {
        'fb_id': 10205447047469248
    }},
    // Expand the scores array into a stream of documents
    { $unwind: '$posts' },
    { $unwind: '$posts.likes.data' },
    { $group: { _id: "$posts.likes.data.id", total: { $sum: 1 }  }},
    { $sort: { total: -1 } },
    //,
    //
    //{ $project: {"posts.post_id" : 1 ,"posts.likes.data.id" : 1 , fb_id : 1 }},
    //{ $unwind: '$posts.likes.data' },
    //{$out:'try_1'}
    ]

)