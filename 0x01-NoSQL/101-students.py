#!/usr/bin/env python3
"""
Top students module
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score
    """
    pipeline = [
        {
            "$project": {
                '_id': 1,
                "name": 1,
                "averageScore": {"$avg": "$topics.score"},
                "topics": 1
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ]

    result = list(mongo_collection.aggregate(pipeline))

    return result
