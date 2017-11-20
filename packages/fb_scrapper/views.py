from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
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
    templ = 'fb_scrapper/scrapper.html'  # template name
    ctx = {  # context
    }
    return render(request, templ, ctx)


# @login_required
def get_fb_scrapper_data(request):
    token_expired = True    # initially assumed no token
    
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
            # need to check if token expired or not
            token_details = get_fb_json_data_from_long_token(
                secret_id=saved_auth.app_secret_id,
                app_id=saved_auth.app_id,
                temp_token=saved_auth.token
            )
            
            # check if token expired
            if  token_details:
                token_expired = False
            form = FbScrapperAuthForm(instance=saved_auth)

    templ = 'fb_scrapper/scrapper-form.html'  # template name
    ctx = {  # context
        "form" : form,
        "form2" : form2,
        "token_expired" : token_expired
    }
    return render(request, templ, ctx)


def scrapper_ajax (request):
    if request.method == 'GET':
        ajax_data = request.GET
        # print(q.get("temp_token"))

        saved_auth = FacebookAuth.objects.first()

        if saved_auth:
            jd = get_fb_json_data_from_long_token(
                secret_id=saved_auth.app_secret_id,
                app_id=saved_auth.app_id,
                temp_token=ajax_data.get("temp_token")
            )
        else:
            jd = {
                "new" : "joldi ekta noya app lo"
            }

        #jd = get_fb_json_data(fb_input_data)
        # print("baal koro?" if not jd else "maal ta hocche: ", jd)
        
        return JsonResponse(jd)
    
    return JsonResponse({
        "error": "baaaaler kono Data not found"
    })


def get_fb_json_data_from_long_token(secret_id=None, app_id=None, temp_token=None):
    fb_dict_input = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": secret_id,
        "fb_exchange_token": temp_token
    }
    
    # url = "https://graph.facebook.com/oauth/access_token?
    # grant_type=fb_exchange_token&client_id=1234&client_secret=a92e&fb_exchange_token=EAAFIx
    
    # generating url to get facebook longtime token
    url_prefix = "https://graph.facebook.com/oauth/access_token?"
    url = url_prefix + '&'.join("{}={}".format(key, fb_dict_input[key]) for key in fb_dict_input)
    
    print("the asshole URL is: ---", url)
    
    r = requests.get(url)
    json_data = json.loads(r.text)
    print("returned JSON data from facebook: " , json_data)
    if json_data.get('error'):
        return False
    else:
        token = json_data.get('access_token')
        update_fb_auth_model(token)
        return token


def update_fb_auth_model(new_token):
    old_obj = FacebookAuth.objects.first()  # save old data for later usage
    FacebookAuth.objects.all().delete()  # no need previous auth tokens
    
    # new instance with new token
    obj = FacebookAuth(
        token=new_token,
        app_id=old_obj.app_id,
        app_secret_id=old_obj.app_secret_id
    )
    obj.save()
