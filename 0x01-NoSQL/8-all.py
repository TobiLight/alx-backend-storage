#!/usr/bin/env python3
"""
List all module
"""


def list_all(mongo_collection):
    """
    Lists all documents in a collection.
    """
    return [collection for collection in mongo_collection.find()]
