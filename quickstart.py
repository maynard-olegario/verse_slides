from __future__ import print_function
import pickle
import os.path
import biblegateway
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/presentations.readonly']

# The ID of a sample presentation.
PRESENTATION_ID = '1EAYk18WDjIG-zp_0vLm3CsfQh_i8eXc67Jo2O9C6Vuc'

def main():
    citations = get_citations('./verses.txt')
    passages = get_passages(citations)
    print(passages)

def get_citations(filename):
    f = open(filename, 'r')
    citations = []
    for line in f:
        citations.append(line)
    return citations

def get_passages(citations):
    default_version = 'NKJV'
    INCLUDE_VERSE = True
    INCLUDE_TITLE = False
    passages = []
    for c in citations:
        p = biblegateway.get_passage(c, default_version, INCLUDE_VERSE, INCLUDE_TITLE)
        passages.append(p)
    return passages

def get_slides():
    """Shows basic usage of the Slides API.
    Prints the number of slides and elments in a sample presentation.
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
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('slides', 'v1', credentials=creds)

    # Call the Slides API
    presentation = service.presentations().get(
        presentationId=PRESENTATION_ID).execute()
    slides = presentation.get('slides')

    print('The presentation contains {} slides:'.format(len(slides)))
    for i, slide in enumerate(slides):
        print('- Slide #{} contains {} elements.'.format(
            i + 1, len(slide.get('pageElements'))))


if __name__ == '__main__':
    main()
