import json

import boto3
from google.oauth2 import service_account
import pandas as pd

from db import Database
from size_analysis import size_analysis
from hazard_analysis import hazard_analysis
from most_active_day import most_active_day


def prepare_asteroid_data(asteroids):
    df = pd.json_normalize(asteroids)

    # remove the close_approach_data column from the df
    df = df.drop(columns=['close_approach_data'])

    # only keep window of data between last 4 weeks and next 4 weeks based on date field
    df['date'] = pd.to_datetime(df['date'])
    oldest_date = pd.to_datetime('now', utc=True) - pd.Timedelta(weeks=4)
    newest_date = pd.to_datetime('now', utc=True) + pd.Timedelta(weeks=4)
    df = df[(df['date'] >= oldest_date) & (df['date'] <= newest_date)]

    # get dataframe for dates in the past 4 weeks
    df_past = df[df['date'] < pd.to_datetime('now', utc=True)]

    # get dataframe for dates in the next 4 weeks
    df_future = df[df['date'] > pd.to_datetime('now', utc=True)]

    return df, df_past, df_future

def lambda_handler(event, context):
    secrets_manager = boto3.client('secretsmanager')

    # Get Google Cloud Service Account Key from Secrets Manager
    GOOGLE_SECRET = secrets_manager.get_secret_value(SecretId='GOOGLE_APPLICATION_CREDENTIALS')
    GOOGLE_APPLICATION_CREDENTIALS = json.loads(GOOGLE_SECRET['SecretString'])

    # Get Google Cloud Datastore Client
    credentials = service_account.Credentials.from_service_account_info(GOOGLE_APPLICATION_CREDENTIALS)

    database = Database(credentials)
    asteroids = database.get_asteroids()
    df, df_past, df_future = prepare_asteroid_data(asteroids)

    last_month = {}
    today = {}
    next_month = {}

    last_month['size_analysis'] = size_analysis(df_past)
    today['size_analysis'] = size_analysis(df)
    next_month['size_analysis'] = size_analysis(df_future)

    last_month['hazard_analysis'] = hazard_analysis(df_past)
    today['hazard_analysis'] = hazard_analysis(df)
    next_month['hazard_analysis'] = hazard_analysis(df_future)

    last_month['most_active_day'] = most_active_day(df_past)
    next_month['most_active_day'] = most_active_day(df_future)

    data = {
        'last_month': last_month,
        'today': today,
        'next_month': next_month
    }

    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }

if __name__ == "__main__":
    print(lambda_handler(None, None))