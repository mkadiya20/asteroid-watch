# Asteroid Watch

## Features
- Get live information on asteroids for the last month and the next month.
- Size analysis: Get data on the largest, smallest, and the average sizes of asteroids.
- Hazard analysis: Get the number of hazardous asteroids
- Most active day: Get the date of most asteroid activity observed.
- Simply enter this on any terminal/command prompt: `curl -X GET "https://0cyd3zrcl8.execute-api.us-east-2.amazonaws.com/Prod/asteroid_watch"
`

## Developer Notes
- Deployed a serverless application using python-based lambda functions.
- Containerized the application using Docker.
- Utilized AWS secrets manager to store `api_key` and `google service account credentials`.
- Connected to Google Datastore as a NoSQL database to store all asteroid data.
- [NASA Near Earth Object Web Service (NeoWs) API](https://api.nasa.gov/)
