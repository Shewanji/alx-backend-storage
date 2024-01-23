#!/usr/bin/env python3
"""module for a  function that returns all students sorted by average score"""


def top_students(mongo_collection):
    """
    function that returns all students sorted by average score
    """

    pipeline = [
        {
            "$project": {
                "name": 1,
                "topics": 1,
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ]

    result = list(mongo_collection.aggregate(pipeline))
    return result
