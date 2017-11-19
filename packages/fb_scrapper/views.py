from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main_app.models import Post, Category, Categorize
from .models import FacebookAuth
from .forms import FbScrapperAuthForm, FbScrapperDataForm
import requests, json


# https://graph.facebook.com/v2.6/oyvai/posts/?fields=full_picture&limit=20&access_token=


# @login_required
def home(request):
    auth = FacebookAuth.objects.all()
    
    templ = 'fb_scrapper/index.html'  # template name
    ctx = {  # context
        "auth_info": auth
    }
    return render(request, templ, ctx)


def scrapper(request):
    fb_input_data = {
        "grant_type": "fb_exchange_token",
        "client_id": "361495860961861",
        "client_secret": "a9255cff275001c025d19f69924eef6e",
        "fb_exchange_token": "ABSCSDQW123123"
    }
    
    jd = get_fb_json_data(fb_input_data)
    print("baal koro ? " if jd["error"] else "maal ta hocche: ", jd)
    
    templ = 'fb_scrapper/scrapper.html'  # template name
    ctx = {  # context
    }
    return render(request, templ, ctx)


def get_fb_json_data(fb_dict_input):
    # url = "https://graph.facebook.com/oauth/access_token?
    # grant_type=fb_exchange_token&client_id=1234&client_secret=a92e&fb_exchange_token=EAAFIx
    
    # generating url to get facebook longtime token
    url_prefix = "https://graph.facebook.com/oauth/access_token?"
    url = url_prefix + '&'.join("{}={}".format(key, fb_dict_input[key]) for key in fb_dict_input)
    
    r = requests.get(url)
    return json.loads(r.text)  # json data


# @login_required
def get_fb_scrapper_data(request):
    if request.method == 'POST':
        form = FbScrapperAuthForm(request.POST)
        form2 = FbScrapperDataForm(request.POST)
        if form.is_valid() and form2.is_valid():
            FacebookAuth.objects.all().delete()     # no need previous auth tokens
            form.save()     # save new token
            form2.save()     # save page info
            return HttpResponseRedirect('/fbs')
        else:
            print(type(form.errors))
    else:
        form2 = FbScrapperDataForm()
        saved_auth = FacebookAuth.objects.first()
        if saved_auth is None:
            form = FbScrapperAuthForm()
        else:
            form = FbScrapperAuthForm(instance=saved_auth)

    templ = 'fb_scrapper/scrapper-form.html'  # template name
    ctx = {  # context
        "form" : form,
        "form2" : form2,
    }
    return render(request, templ, ctx)
