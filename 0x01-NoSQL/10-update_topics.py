#!/usr/bin/env python3
"""
Update topics module
"""


def update_topics(mongo_collection, name, topics):
    """
    Changes all topics of a school document based on the name
    """
    data = mongo_collection.update(
        {'name': name}, {'$set': {'topics': topics}})
    return data
