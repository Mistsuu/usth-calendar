from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import sys
import datetime
import pickle
import os.path

# If modifying the SCOPES array, delete the file token.pickle.
SCOPES     = ['https://www.googleapis.com/auth/calendar']
exceptions = \
{
    'dXN0aC5lZHUudm5fcWkzZmRsMmRmbWhybnZ2Y2ZobzJqNjdpZTRAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ': 'usth.edu.vn_qi3fdl2dfmhrnvvcfho2j67ie4@group.calendar.google.com'
}
service    = None
nUpcoming  = int(sys.argv[1]) # Number of upcoming events

"""
    auth():
        Authenticate the calendar with the token.pickle file
"""
def auth():
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

"""
    get_calendar_by_id():
        Print the <nUpcoming> events from a calendar identified by the <calendar_id>
        The print format is like the following:
        [Start time], [End time], [Summary], [Location], [Description]

        [Parameters]:
            calendar_id: ID of the calendar we want to print the data from.
"""
def print_calendar_by_id(calendar_id):
    # Get current datetime
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    
    # Retrieve the <nUpcoming> upcoming events
    events_result = service.events().list   \
    (       calendarId   = calendar_id, 
            timeMin      = now,
            maxResults   = nUpcoming, 
            singleEvents = True,
            orderBy      = 'startTime'
    ).execute()

    # Print event data 
    events = events_result.get('items', [])
    if not events or len(events) == 0:
        print('No upcoming events found.')
    for event in events:
        print(
            "\"\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\"".format(
                event.get('start').get('dateTime', event.get('start').get('date')),
                event.get('end').get('dateTime', event.get('end').get('date')),
                event.get('summary'),
                event.get('location'),
                event.get('description')
            )
        )
    print()

"""
    get_query():
        Getting the query value of a key from an URL query string.

        [Parameters]:
            url: The input URL string.
            key: The key we want to find the value.
"""
def get_query(url, key):
    value = ''
    if '?' + key + '=' in url:
        value = url.split('?' + key + '=')[1].split('&')[0]
    elif '&' + key + '=' in url:
        value = url.split('&' + key + '=')[1].split('&')[0]
    return value

"""
    get_calendar_id():
        Get the calendar ID from a calendar URL.

        [Parameters]:
            calendar_url: URL of the calendar we want to get the ID from.
"""
def get_calendar_id(calendar_url):
    # Get 'src' query
    calendar_id = get_query(calendar_url, 'src')

    # Checks exceptions (might investigate later :p)
    if calendar_id in exceptions:
        calendar_id = exceptions[calendar_id]

    # Replace special characters
    calendar_id = calendar_id.replace('%40', '@')
    return calendar_id


"""
    main():
        Main function of the program.

        [Parameters]:
            URLFile: The file containing an URL list that has the URLs of the calendars.
                     Obtained by running "python ./get_link_calendar.py" first.
"""
def main(URLFile):
    # Authenticate with Google API.
    auth()

    print('* '+ str(sys.argv[1]) + ' events from upcoming calendar:')
    print('"Calendar Name", "Start Time", "End Time", "Subjects", "Location", "Description"')
    
    # Getting the url list from scraped websites
    with open(URLFile, 'r') as calendar_file:
        for line in calendar_file:
            groups       = line.split(' ')
            title        = ' '.join(groups[:-1])
            calendar_url = groups[-1][:-1]

            print(title + ":")
            try:
                print_calendar_by_id(get_calendar_id(calendar_url))
            except KeyboardInterrupt:
                exit(-1)
            except Exception as e:
                print("Cannot query the calendar.\n")
                sys.stderr.write("[!]", e)
                pass

if __name__ == '__main__':
    main('./calendar_urls.txt')
