#!/usr/bin/env python3
"""
Insert school module
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection
    """
    data = mongo_collection.insert_one(kwargs)
    return data.inserted_id
