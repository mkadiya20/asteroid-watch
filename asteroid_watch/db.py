from datetime import datetime

from google.cloud import datastore

class Database:
    def __init__(self, credentials):
        self.credentials = credentials
        self.client = datastore.Client(credentials=credentials)

    def get_asteroids(self):
        query = self.client.query(kind='asteroids')
        return list(query.fetch())