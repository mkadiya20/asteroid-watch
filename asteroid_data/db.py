from datetime import datetime

from google.cloud import datastore

class Database:
    def __init__(self, credentials):
        self.credentials = credentials
        self.client = datastore.Client(credentials=credentials)

    def check_date(self, date):
        """Check if the given date is already present in the database"""
        query = self.client.query(kind='asteroids')

        # Convert the date to datetime.datetime object
        datetime_date = datetime.combine(date, datetime.min.time())

        # Set filter and order
        query.add_filter('date', '<=', datetime_date)

        # retrieve the first result
        result = list(query.fetch())
        
        print(result)
    
    def put_new_data(self, data):
        """Put new data into datastore"""
        asteroids = []
        dates = data['near_earth_objects'].keys()
        for date in dates:
            for asteroid in data['near_earth_objects'][date]:
                # add datetime object to asteroid data
                asteroid['date'] = datetime.strptime(date, '%Y-%m-%d')
                asteroids.append(asteroid)

        # add asteroid data to datastore
        for asteroid in asteroids:
            # check if asteroid already exists in datastore
            key = self.client.key('asteroids', asteroid['neo_reference_id'])
            document = self.client.get(key=key)

            if document is None:
                entity = datastore.Entity(key=key)
                entity.update(asteroid)
                self.client.put(entity)
            else:
                print(f'Asteroid {asteroid["neo_reference_id"]} already exists in datastore')
