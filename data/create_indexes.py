import os

import pymongo
from pymongo import MongoClient
from pymongo.errors import OperationFailure

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('MONGODB_DB_NAME', 'iteso')


connection = MongoClient(MONGODB_URI);
db = connection.get_database(DB_NAME);

collection = db.books;

try:
    collection.create_index([('average_rating', pymongo.DESCENDING)], name='AverageRatingIndex')
    collection.create_index([('ratings_count', pymongo.DESCENDING)], name='RatingsCountIndex')
    collection.create_index([('text_reviews_count', pymongo.DESCENDING)], name='TextReviewsCountIndex')
    collection.create_index([('title', pymongo.ASCENDING)], name='TitleIndex', default_language='english')
    print("Indexes created..")
except OperationFailure as oe:
    print("Indexes alread exits")

print(collection.index_information())
