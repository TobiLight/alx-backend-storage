#!/usr/bin/env python3
"""
Schools by topic module
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of school having a specific topic
    """
    data = mongo_collection.find({'topic': topic})
    return list(data)
