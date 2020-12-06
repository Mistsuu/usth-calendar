from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import sys
import datetime
import pickle
import os.path

# If modifying these scopes, delete the file token.pickle.
SCOPES     = ['https://www.googleapis.com/auth/calendar']
exceptions = \
{
    'dXN0aC5lZHUudm5fcWkzZmRsMmRmbWhybnZ2Y2ZobzJqNjdpZTRAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ': 'usth.edu.vn_qi3fdl2dfmhrnvvcfho2j67ie4@group.calendar.google.com'
}
service    = None
N          = int(sys.argv[1]) # Number of upcoming events

def auth():
    """
        Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow  = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Get service from creds
    global service
    service = build('calendar', 'v3', credentials=creds)

# Call the Calendar API
def get_calendar_by_id(calendar_id):
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId=calendar_id, timeMin=now,
                                          maxResults=N, singleEvents=True,
                                          orderBy='startTime').execute()

    # Print event lists
    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def get_query(url, key):
    # Split string
    value = ''
    if '?' + key + '=' in url:
        value = url.split('?' + key + '=')[1].split('&')[0]
    elif '&' + key + '=' in url:
        value = url.split('&' + key + '=')[1].split('&')[0]
    return value

def get_calendar_id(calendar_url):
    # Get 'src' query
    calendar_id = get_query(calendar_url, 'src')

    # Checks exceptions (might investigate later :p)
    if calendar_id in exceptions:
        calendar_id = exceptions[calendar_id]

    # Replace special characters
    calendar_id = calendar_id.replace('%40', '@')
    return calendar_id


def main():
    # Authenticate
    auth()

    # Getting the url list from scraped websites
    print('* '+ str(sys.argv[1]) + ' events from upcoming calendar:')
    with open('calendar_urls.txt', 'r') as calendar_file:
        for line in calendar_file:
            groups       = line.split(' ')
            title        = ' '.join(groups[:-1])
            calendar_url = groups[-1][:-1]

            print("///////////////////////////////////////////////\n[+] " + title + ":")
            try:
                get_calendar_by_id(get_calendar_id(calendar_url))
            except KeyboardInterrupt:
                exit(-1)
            except:
                pass

if __name__ == '__main__':
    main()
