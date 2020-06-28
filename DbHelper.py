import pymongo
import os

db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

def connect():
  ## mongodb+srv://{}:{}@mongocluster-1n5ld.mongodb.net/test?retryWrites=true&w=majority
  db_connection = "mongodb+srv://{}:{}@mongocluster-1n5ld.mongodb.net/".format(db_username, db_password)
  client = pymongo.MongoClient(db_connection)

  if db_name not in client.list_database_names():
    Exception('DB DOES NOT EXIST')
  return client[db_name]