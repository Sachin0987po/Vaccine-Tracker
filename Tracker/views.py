from django.shortcuts import render, HttpResponse
from django.utils.timezone import datetime, timedelta
from django.contrib.sites.shortcuts import get_current_site
from .models import userEntry
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from cowin_api import CoWinAPI
from background_task import background
from .task import *

def home(request):
    return render(request, 'index.html')


def entry(request):
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        pincode = request.POST['pincode']
        dose_type = request.POST['dose_type']
        min_age_limit = request.POST['min_age_limit']
        
        context = {
            'name' : name,
            'email' : email,
            'pincode' : pincode,
            'dose_type' : dose_type,
            'min_age_limit' : min_age_limit
        }

        if userEntry.objects.filter(email = email, min_age_limit = min_age_limit, pincode = pincode, dose_type = dose_type).exists():
            return render(request, 'alreadyregister.html')
        
        userEntry(name = name, email = email, pincode = pincode, dose_type = dose_type, min_age_limit = min_age_limit).save()
        return render(request, 'success.html', context)
    
    else:
        return render(request, 'index.html')



