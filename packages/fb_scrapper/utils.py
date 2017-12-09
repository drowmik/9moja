import urllib.request, requests, json, os
from core.settings import MEDIA_ROOT
from django.utils import timezone
from main_app.models import Post, Category, Categorize
from .models import FacebookAuth, ScrappedData


def get_long_token(fb_auth_model, secret_id=None, app_id=None, temp_token=None):
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
    
    print("the fb graph api URL is: ---", url)
    
    r = requests.get(url)
    json_data = json.loads(r.text)
    print("returned JSON data from facebook: ", json_data)
    if not json_data.get('error'):
        token = json_data.get('access_token')
        
        # update_fb_auth_model
        old_obj = fb_auth_model.objects.first()  # save old data for later usage
        fb_auth_model.objects.all().delete()  # no need previous auth tokens
        
        # new instance with new token
        obj = fb_auth_model(
            token=token,
            app_id=old_obj.app_id,
            app_secret_id=old_obj.app_secret_id
        )
        obj.save()
    return json_data


def scrap_data(api_ver="v2.11", page="", limit="100", fields=("full_picture",), token=""):
    if not token:
        # token/ auth error
        return {
            "error": {
                "message": "No Auth/Token found"
            }
        }
    
    if int(limit) > 100:
        return {
            "error": {
                "message": "Maximum limit is 100"
            }
        }
    
    # https://graph.facebook.com/v2.6/oyvai/posts/?fields=full_picture&limit=20&access_token=
    # generating url to to scrap data from facebook
    url_prefix = "https://graph.facebook.com/" + api_ver + "/" + page + "/posts/?fields="
    url = url_prefix + ','.join("{}".format(f) for f in fields)
    url += "&access_token=" + token + "&limit=" + limit
    
    return get_data_by_url(url)


def get_data_by_url(url):
    r = requests.get(url)
    data = json.loads(r.text)
    for k in data['data']:
        if k['type'] == 'photo':
            share = (k.get('shares')['count'] / 10) if k.get('shares') else 0
            likes = (k.get('reactions').get('summary')['total_count'] / 100) if k.get('reactions').get('summary')['total_count'] else 0
            k['score'] = share + likes
        else:
            # remove non photo objects
            data['data'].remove(k)
    
    # sort the json data by the score
    data['data'].sort(key=lambda d: d.get('score', 111))
    
    return data


def get_data_by_page_name(page=None, direct_url=None):
    if direct_url:
        jd = get_data_by_url(direct_url)
    else:
        token = FacebookAuth.objects.first().token
        fields = {
            "full_picture",
            "type",
            "reactions.summary(true)",
            "shares",
        }
        
        # default limit 100
        jd = scrap_data(
            page=page,
            fields=fields,
            token=token
        )
    
    return jd


def save_fb_scrapper_all_img_by_url(img_url_list, category_name, img_details=None):
    for i, item in enumerate(img_url_list):
        dir = os.path.join(
            MEDIA_ROOT,  # media/
            timezone.now().date().isoformat(),  # YYYY-MM-DD/
        )  # directory string
        
        # create directory if not exists
        if not os.path.exists(dir):
            os.makedirs(dir)
        
        # posts under this category for unique image name
        try:
            count = Categorize.objects.filter(
                category=Category.objects.get(name=category_name)
            ).__len__()
        except:
            count = 0
        
        # unique image name
        if count:
            slug = category_name + "-" + str(count + i)
        else:
            slug = category_name + "-" + str(i)
        
        img_dir = os.path.join(timezone.now().date().isoformat(), slug + ".jpg")
        
        if img_details:
            # getting all post_id in an dict
            # but each post_id is in tuple
            # converting tuple into string
            old_f = [''.join(t) for t in [x for x in ScrappedData.objects.all().values_list('post_id')]]
            
            # save only if the image is new
            if img_details['id'][i] not in old_f:
                f = ScrappedData(
                    post_id=img_details['id'][i],
                    shares=img_details['shares'][i],
                    likes=img_details['likes'][i],
                    score=img_details['score'][i],
                )
                f.save()
            else:
                return None
        else:
            return None
        
        # download the image
        # scrapped data from facebook always jpg
        urllib.request.urlretrieve(item, os.path.join(dir, slug + ".jpg"))
        
        # creating a post instance and save
        p = Post(
            slug=slug,
            title=slug,
            img=img_dir,
            publish_date=timezone.now(),
            status="p",
        )
        p.save()
        
        new_cat, created = Category.objects.update_or_create(name=category_name)
        
        # connecting post and category
        Categorize.objects.update_or_create(
            post=p,
            category=Category.objects.get(id=new_cat.id),
        )
