import requests, json
from .models import FacebookAuth


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
            share = (k['shares']['count'] / 10) if k.get('shares') else 0
            likes = (k['reactions']['summary']['total_count'] / 100) if k['reactions']['summary']['total_count'] else 0
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
        jd = scrap_data(
            page=page,
            fields=fields,
            token=token
        )
    
    return jd