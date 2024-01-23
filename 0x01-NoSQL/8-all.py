#!/usr/bin/env python3
""" module to List all documents """


def list_all(mongo_collection):
    """
    function that lists all documents in a collection
    """

    documents = list(mongo_collection.find({}))
    return documents
