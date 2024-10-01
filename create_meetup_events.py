import requests
import csv
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Function to read events from CSV file
def read_events_from_csv(file_path):
    events = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            events.append(row)
    return events

# Function to upload event picture
def upload_event_picture(api_key, group_urlname, picture_path):
    url = f'https://api.meetup.com/{group_urlname}/photo_upload'
    files = {'photo': open(picture_path, 'rb')}
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.post(url, files=files, headers=headers)
    if response.status_code == 201:
        return response.json()['id']
    else:
        print(f'Failed to upload picture: {response.status_code}')
        print(response.json())
        return None

# Read events from events.csv
events = read_events_from_csv('events.csv')

# Meetup API key
api_key = os.getenv('MEETUP_API_KEY')

# Iterate over each event and post it to Meetup
for event in events:
    group_urlname = event['group_urlname']
    event_name = event['name']
    event_description = event['description']
    event_time = int(datetime.strptime(event['time'], '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
    event_duration = int(event['duration']) * 60 * 1000  # Convert minutes to milliseconds
    venue_id = event['venue_id']
    rsvp_limit = event['rsvp_limit']
    picture_path = event.get('picture_path', None)

    # Upload event picture and get the photo ID if picture_path is provided
    photo_id = None
    if picture_path:
        photo_id = upload_event_picture(api_key, group_urlname, picture_path)

    # Define the event data
    event_data = {
        'name': event_name,
        'description': event_description,
        'time': event_time,
        'duration': event_duration,
        'venue_id': venue_id,
        'rsvp_limit': rsvp_limit,
        'draft': True,  # Save event as draft
    }

    # Add photo_id to event_data if it exists
    if photo_id:
        event_data['photo_id'] = photo_id

    # Preview the event details

    # Define the URL for creating an event
    url = f'https://api.meetup.com/{group_urlname}/events'

    # Make the POST request to create the event
    response = requests.post(url, json=event_data, headers={'Authorization': f'Bearer {api_key}'})

    # Check the response
    if response.status_code == 201:
        print(f'Event "{event_name}" created successfully as draft!')
    else:
        print(f'Failed to create event "{event_name}": {response.status_code}')
        print(response.json())
