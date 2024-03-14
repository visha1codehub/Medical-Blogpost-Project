from datetime import datetime, timedelta
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def build_service():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  service = build("calendar", "v3", credentials=creds)
  return service


def create_event(appointment):
  service = build_service()

  date = appointment.date
  start_time = appointment.start_time
  end_time = appointment.end_time
  summary = appointment.patient.full_name
  start_datetime_iso = datetime.combine(date, start_time).isoformat()
  end_datetime_iso = datetime.combine(date, end_time).isoformat()
  calendar_id = appointment.doctor.calendar_id
  print(start_datetime_iso)
  event = {
			'summary': summary,
			'start': {
					'dateTime': start_datetime_iso,
					'timeZone': 'Asia/Kolkata',
			},
			'end': {
					'dateTime': end_datetime_iso,
					'timeZone': 'Asia/Kolkata',
			},
  }
  service.events().insert(calendarId=calendar_id, body=event).execute()


def create_calendar_id(summary):
  service = build_service()
  new_calendar = {
      'summary': summary,
      'timeZone': 'Asia/Kolkata'
  }
  created_calendar = service.calendars().insert(body=new_calendar).execute()
  # print(created_calendar)
  print(f"Created calendar: {created_calendar['id'], created_calendar['summary']}")
  return created_calendar['id']


if __name__ == "__main__":
  create_calendar_id("main")