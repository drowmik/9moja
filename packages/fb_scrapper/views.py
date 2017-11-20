from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main_app.models import Post, Category, Categorize
from .models import FacebookAuth
from .forms import FbScrapperAuthForm, FbScrapperDataForm
import requests, json


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
def get_fb_scrapper_auth(request):
    token_expired = True  # initially assumed no token
    
    if request.method == 'POST':
        form = FbScrapperAuthForm(request.POST)
        # form2 = FbScrapperDataForm(request.POST)
        # print(form["app_secret_id"].value())
        if form.is_valid():  # and form2.is_valid():
            FacebookAuth.objects.all().delete()  # no need previous auth tokens
            form.save()  # save new token
            # form2.save()     # save page info
            if form["token"].value():
                return HttpResponseRedirect('/fbs/')
            else:
                return HttpResponseRedirect('/fbs/scrapper-auth-form/')
        else:
            print(type(form.errors))
    else:
        # form2 = FbScrapperDataForm()
        
        saved_auth = FacebookAuth.objects.first()
        if saved_auth is None:
            form = FbScrapperAuthForm()
        else:
            # need to check if token expired or not
            token_details = get_long_token(
                secret_id=saved_auth.app_secret_id,
                app_id=saved_auth.app_id,
                temp_token=saved_auth.token
            )
            
            # check if token expired
            if not token_details.get('error'):
                token_expired = False
            form = FbScrapperAuthForm(instance=saved_auth)
    
    templ = 'fb_scrapper/scrapper-auth-form.html'  # template name
    ctx = {  # context
        "form": form,
        # "form2" : form2,
        "token_expired": token_expired
    }
    return render(request, templ, ctx)


def get_fb_scrapper_data(request):
    if request.method == 'POST':
        form = FbScrapperDataForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/fbs/')
    else:
        if not FacebookAuth.objects.first():
            return HttpResponseRedirect('/fbs/scrapper-auth-form/')
        else:
            form = FbScrapperDataForm()

    templ = 'fb_scrapper/scrapper-data-form.html'  # template name
    ctx = {  # context
        "form": form
    }
    return render(request, templ, ctx)


def scrapper_ajax(request):
    if request.method == 'GET':
        ajax_data = request.GET
        
        saved_auth = FacebookAuth.objects.first()
        # if any auth is saved just change the token
        if saved_auth:
            jd = get_long_token(
                secret_id=saved_auth.app_secret_id,
                app_id=saved_auth.app_id,
                temp_token=ajax_data.get("temp_token")
            )
        else:
            jd = {
                "error": {
                    "message": "Add new app ID and app secret ID First"
                }
            }
        
        print("json data dicchi ajax re ...", jd)
        
        # jd = get_fb_json_data(fb_input_data)
        # print("baal koro?" if not jd else "maal ta hocche: ", jd)
        
        return JsonResponse(jd)
    
    return JsonResponse({
        "error": {
            "message": "Data not found"
        }
    })


def get_data_ajax(request):
    jd = {}
    if request.method == 'GET':
        page_data = request.GET
        field = []
        for x in dict(page_data):
            if x[:5] == "field":
                print("voda paisi amar baaaaaaal:    ", page_data.get(x))
                field.append(page_data.get(x))
        if FacebookAuth.objects.first():
            token = FacebookAuth.objects.first().token
            jd = scrap_data(
                page=page_data.get("page"),
                limit=page_data.get("limit"),
                fields=field,
                token=token
            )
            print(jd)
        else:
            return HttpResponseRedirect('/fbs/scrapper-auth-form/')
    else:
        jd = {
            "error": {
                "message": "Broken Url.."
            }
        }
        
    return JsonResponse(jd)


def get_long_token(secret_id=None, app_id=None, temp_token=None):
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
    
    # print("the URL is: ---", url)
    
    r = requests.get(url)
    json_data = json.loads(r.text)
    print("returned JSON data from facebook: ", json_data)
    if not json_data.get('error'):
        token = json_data.get('access_token')
        update_fb_auth_model(token)
    return json_data


def scrap_data(api_ver="v2.11", page="", limit="500",fields=("full_picture",), token=""):
    if not token:
        # token/ auth error
        return {
                "error": {
                    "message": "No Auth/Token found"
                }
            }

    # https://graph.facebook.com/v2.6/oyvai/posts/?fields=full_picture&limit=20&access_token=
    # generating url to to scrap data from facebook
    url_prefix = "https://graph.facebook.com/" + api_ver + "/" + page + "/posts/?fields="
    url = url_prefix + ','.join("{}".format(f) for f in fields)
    url += "&access_token=" + token + "&limit=" + limit
    
    print("the URL is: -----", url)
    
    r = requests.get(url)
    json_data = json.loads(r.text)
    print("returned JSON data from facebook: ", json_data)
    
    return json_data


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
