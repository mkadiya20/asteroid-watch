import asyncio
import json

import boto3
from google.oauth2 import service_account
from google.auth.transport.requests import Request

from db import Database
from api import get_weekly_window, get_asteroid_data

async def process_weekly_data(start_date, end_date, NASA_API_KEY, credentials):
    database = Database(credentials)
    data = await get_asteroid_data(start_date, end_date, NASA_API_KEY)
    database.put_new_data(data)

async def main():
    secrets_manager = boto3.client('secretsmanager')

    # Get NASA API Key from Secrets Manager
    NASA_SECRET = secrets_manager.get_secret_value(SecretId='NASA_API_KEY')
    NASA_API_KEY = json.loads(NASA_SECRET['SecretString'])['NASA_API_KEY']

    # Get Google Cloud Service Account Key from Secrets Manager
    GOOGLE_SECRET = secrets_manager.get_secret_value(SecretId='GOOGLE_APPLICATION_CREDENTIALS')
    GOOGLE_APPLICATION_CREDENTIALS = json.loads(GOOGLE_SECRET['SecretString'])

    # Get Google Cloud Datastore Client
    credentials = service_account.Credentials.from_service_account_info(GOOGLE_APPLICATION_CREDENTIALS)

    # Get access token
    target_scopes = ['https://www.googleapis.com/auth/datastore']
    credentials = credentials.with_scopes(target_scopes)
    request = Request()
    credentials.refresh(request)

    weeks = get_weekly_window()
    tasks = []

    for week in weeks:
        task = asyncio.create_task(process_weekly_data(week['start_date'], week['end_date'], NASA_API_KEY, credentials))
        tasks.append(task)

    # Wait for all tasks to complete
    await asyncio.gather(*tasks)

def lambda_handler(event, context):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

if __name__ == "__main__":
    # Invoke the main function when running the script directly
    asyncio.run(main())