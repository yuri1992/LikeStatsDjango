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
    
    db.getCollection('users').aggregate([
    { $match: {
        'fb_id': 10205447047469250
    }},
    // Expand the scores array into a stream of documents
    { $unwind: '$videos' },
    { $unwind: '$videos.likes.data' },
    { $group: {
            
        } },
    { $sort: {
        
        } }
    ],
    {
        explain:true,
        out:'total_likes'
    }
)