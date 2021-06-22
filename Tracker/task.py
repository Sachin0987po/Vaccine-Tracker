from django.utils.timezone import datetime, timedelta
from .models import userEntry
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from background_task import background
from django.utils.html import strip_tags
from vaccineTracker import settings
import requests
import json

def sentmail(entry, centers):
    mail_subject = 'Vaccine Tracker'
    html_message = render_to_string('mail.html', {
        'user': entry.name,
        'dose_type' : entry.dose_type,
        'centers' : centers
    })
    text_message = strip_tags(html_message)
    to_email = entry.email
    email = EmailMultiAlternatives(
        mail_subject, text_message, settings.EMAIL_HOST_USER, [to_email] 
    )
    email.attach_alternative(html_message, "text/html")
    email.send()
    entry.delete()


@background(schedule = 0)
def mail():
    entries = userEntry.objects.all()
    for entry in entries:
        date = datetime.today().strftime("%d-%m-%Y")
        pincode = entry.pincode
        base_url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={date}".format(pincode = pincode, date = date)
        available = requests.get(base_url).json()
        centers = []
        
        for data in available['centers']:
            for session in data['sessions']:
                if entry.dose_type == 1:
                    if session['available_capacity_dose1'] > 0:
                        centers.append([data['name'], data['address'], session['date'], data['fee_type'], session['vaccine']])
                else:
                    if session['available_capacity_dose2'] > 0:
                        centers.append([data['name'], data['address'], session['date'], data['fee_type'], session['vaccine']])

        if len(centers) > 0:
            sentmail(entry, centers)
