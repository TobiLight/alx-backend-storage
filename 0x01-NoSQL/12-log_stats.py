#!/usr/bin/env python3
"""
Nginx request logs module
"""
from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    """
    Prints stats about Nginx request logs.
    """
    print('{} logs'.format(nginx_collection.estimated_document_count()))
    print('Methods:')

    for method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
        req_count = nginx_collection.count_documents({"method": method})
        print('\tmethod {}: {}'.format(method, req_count))
    status_checks_count = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print('{} status check'.format(status_checks_count))


if __name__ == '__main__':
    client = MongoClient('mongodb://127.0.0.1:27017').logs.nginx
    print_nginx_request_logs(client)
