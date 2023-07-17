from datetime import datetime, timedelta

import aiohttp

def get_weekly_window():
    """For an 8 week window, return the start and end dates
    for the last 4 weeks and next 4 weeks"""
    date = datetime.date(datetime.now())
    weeks = []
    
    for i in range(-4, 5):
        weeks.append({
            'start_date': date + timedelta(days=7 * i),
            'end_date': date + timedelta(days=7 * i + 6),
        })
    
    return weeks

async def get_asteroid_data(start_date, end_date, api_key):
    """Get asteroid data from NASA API for the given date range"""
    URL = f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}'
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            data = await response.json()
            return data
