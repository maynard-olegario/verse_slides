from __future__ import print_function
import pickle
import os.path
import biblegateway
import pprint
import uuid
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/presentations']

# todo: dynamic presentation_id
PRESENTATION_ID = '12XDv6JAdduXgoTneZdQ9tawfGouTPQLExTUEb3RUurU'


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
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def add_slide(citation='default citation', passage='default passage'):
    service = build('slides', 'v1', credentials=auth())

    # Call the Slides API
    presentation = service.presentations().get(
        presentationId=PRESENTATION_ID).execute()
    slides = presentation.get('slides')

    # pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint (slides)
    # print ('****************')

    titleId = uuid.uuid4().hex
    bodyId = uuid.uuid4().hex
    requests = [
        {
            "createSlide": {
                # "objectId": pageId,
                "slideLayoutReference": {
                    "predefinedLayout": "TITLE_AND_BODY"
                },
                "placeholderIdMappings": [
                    {
                        "layoutPlaceholder": {
                            "type": "TITLE",
                            "index": 0
                        },
                        "objectId": titleId,
                    },
                    {
                        "layoutPlaceholder": {
                            "type": "BODY",
                            "index": 0,
                        },
                        "objectId": bodyId,
                    },
                ],
            }
        },
        {
            "insertText": {
                "objectId": titleId,
                "text": citation,
            }
        },
        {
            "insertText": {
                "objectId": bodyId,
                "text": passage,
            }
        },
        {
            "updateTextStyle": {
                "objectId": titleId,
                "fields": "bold,fontSize",
                "textRange": {
                    "type": "ALL"
                },
                "style": {
                    "bold": True,
                    "fontSize": {
                        "magnitude": 18,
                        "unit": "PT"
                    }
                }
            }
        },
        {
            "updateTextStyle": {
                "objectId": bodyId,
                "fields": "fontFamily,fontSize",
                "textRange": {
                    "type": "ALL"
                },
                "style": {
                    "fontFamily": "Arial",
                    "fontSize": {
                        "magnitude": 18,
                        "unit": "PT"
                    }
                }
            }
        }
    ]

    # If you wish to populate the slide with elements,
    # add element create requests here, using the page_id.

    # Execute the request.
    body = {
        'requests': requests
    }
    response = service.presentations() \
        .batchUpdate(presentationId=PRESENTATION_ID, body=body).execute()
    create_slide_response = response.get('replies')[0].get('createSlide')
    print('Created slide with ID: {0}'.format(
        create_slide_response.get('objectId')))


def get_slides():
    service = build('slides', 'v1', credentials=auth())

    # Call the Slides API
    presentation = service.presentations().get(
        presentationId=PRESENTATION_ID).execute()
    slides = presentation.get('slides')

    print('The presentation contains {} slides:'.format(len(slides)))
    for i, slide in enumerate(slides):
        print('- Slide #{} contains {} elements.'.format(
            i + 1, len(slide.get('pageElements'))))
