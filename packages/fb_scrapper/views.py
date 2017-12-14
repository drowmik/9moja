from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main_app.models import custom_slugify
from django.urls import reverse

from .forms import FbScrapperAuthForm, FbScrapperDataForm
from .utils import *


@login_required
def home(request):
    auth = FacebookAuth.objects.all()
    
    templ = 'fb_scrapper/index.html'  # template name
    ctx = {  # context
        "auth_info": auth
    }
    return render(request, templ, ctx)


@login_required
def scrapper(request):
    templ = 'fb_scrapper/scrapper.html'  # template name
    ctx = {  # context
    }
    return render(request, templ, ctx)


@login_required
def get_fb_scrapper_auth(request):
    token_expired = True  # initially assumed no token
    
    if request.method == 'POST':
        form = FbScrapperAuthForm(request.POST)
        if form.is_valid():
            FacebookAuth.objects.all().delete()  # no need previous auth tokens
            form.save()  # save new token
            if form["token"].value():
                return HttpResponseRedirect('/fbs/')
            else:
                return HttpResponseRedirect('/fbs/scrapper-auth-form/')
        else:
            print(type(form.errors))
    else:
        saved_auth = FacebookAuth.objects.first()
        if saved_auth is None:
            form = FbScrapperAuthForm()
        else:
            # need to check if token expired or not
            token_details = get_long_token(
                FacebookAuth,
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
        "token_expired": token_expired
    }
    return render(request, templ, ctx)


@login_required
def get_fb_scrapper_data(request):
    if request.method == 'POST':
        form = FbScrapperDataForm(request.POST)
        if form.is_valid():
            form.save()
            cat_name = custom_slugify(value=form["name"].value())
            
            img_urls = form["selected_img"].value().split(",")
            # img_react = form["fb_img_reaction"].value().split(",")
            # img_share = form["fb_img_share"].value().split(",")
            
            save_fb_scrapper_all_img_by_url(img_urls, cat_name)
            
            return HttpResponseRedirect(reverse('main_app:each_category', args=[Category.objects.get(name=cat_name).slug]))
    else:
        if not FacebookAuth.objects.first():
            return HttpResponseRedirect('/fbs/scrapper-auth-form/')
        else:
            form = FbScrapperDataForm()
    
    templ = 'fb_scrapper/scrapper-data-form.html'  # template name
    ctx = {  # context
        "form": form,
        "fb_fields": {
            "0": "full_picture",
            "1": "type",
            "2": "reactions.summary(true)",
            "3": "shares",
        },
    }
    return render(request, templ, ctx)


@login_required
def scrapper_ajax(request):
    if request.method == 'GET':
        ajax_data = request.GET
        
        saved_auth = FacebookAuth.objects.first()
        # if any auth is saved just change the token
        if saved_auth:
            jd = get_long_token(
                FacebookAuth,
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
        
        return JsonResponse(jd)
    
    return JsonResponse({
        "error": {
            "message": "Data not found"
        }
    })


@login_required
def get_data_ajax(request):
    if request.method == 'GET':
        page_data = request.GET
        
        if page_data.get("direct_url"):
            d_url = page_data.get("direct_url")
            r = requests.get(d_url)
            json_data = json.loads(r.text)
            return JsonResponse(json_data)
        
        field = []
        # creating field list (fields from ajax request)
        field.extend(
            [page_data.get(x) for x in dict(page_data) if x[:5] == "field"]
        )
        
        if FacebookAuth.objects.first():
            token = FacebookAuth.objects.first().token
            jd = scrap_data(
                page=page_data.get("page"),
                limit=page_data.get("limit"),
                fields=field,
                token=token
            )
            # print(jd)
        else:
            return HttpResponseRedirect('/fbs/scrapper-auth-form/')
    else:
        jd = {
            "error": {
                "message": "Broken Url.."
            }
        }
    
    return JsonResponse(jd)
