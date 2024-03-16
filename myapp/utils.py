from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import os
import google_apis_oauth
from googleapiclient.discovery import build
from datetime import datetime


def paginatePosts(request, posts):
    page = request.GET.get('page')
    paginator = Paginator(posts, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        page=1
        posts = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        posts = paginator.page(page)
    ranges = range(1, paginator.num_pages+1)

    return posts, ranges


def createEvent(appointment):
    token = appointment.doctor.token
    # print(type(token))
    creds, refreshed = google_apis_oauth.load_credentials(token)
    service = build('calendar', 'v3', credentials=creds)


    date = appointment.date
    start_time = appointment.start_time
    end_time = appointment.end_time
    summary = f'{appointment.patient.full_name} : {appointment.speciality}'
    start_datetime_iso = datetime.combine(date, start_time).isoformat()
    end_datetime_iso = datetime.combine(date, end_time).isoformat()
    # print(start_datetime_iso)
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
    service.events().insert(calendarId='primary', body=event).execute()