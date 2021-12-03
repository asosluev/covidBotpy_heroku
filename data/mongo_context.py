import os

from datetime import datetime
from pymongo import MongoClient


class MongoDbContext:
    """Mongo database context class"""

    # constructor of class

    connection_string = os.getenv('CONNECTION_STRING')
    client = MongoClient(connection_string)

    # save user query method
    def save_query(client, country, user_name):
        db = client[os.getenv('DB_NAME')]
        countries_stats = db.country_stats
        result = countries_stats.insert_one({'date': datetime.now(), 'country': country, 'username': user_name})

    # get users queries method
    def get_users_queries(client):
        db = client[os.getenv('DB_NAME')]
        countries_stats = db.country_stats
        queries = countries_stats.aggregate([
            {'$group': {'_id': '$country', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 10}
        ])
        users = countries_stats.aggregate([
            {'$group': {'_id': '$username', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 10}
        ])
        return {'queries': list(queries), 'users': list(users)}