import os
import sys
import signal
import traceback

DATA_MINING_PAGE_DEPTH = 5  # facebook data mining depth page number (100x value)
TOP_POST_NUMBER = 20  # top post for each 100

DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(DIR)
PACKAGE_DIR = os.path.join(BASE_DIR, 'packages')

try:
    import django
except ImportError:
    raise Exception("Failed to import django")
else:
    sys.path.extend([BASE_DIR, PACKAGE_DIR])
    os.environ["DJANGO_SETTINGS_MODULE"] = "core.settings"
    try:
        django.setup()
    except Exception:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)

from core.settings import FB_PAGE_SCRAP_FOR_CRON as fb_pages
from fb_scrapper.utils import get_data_by_page_name, save_fb_scrapper_all_img_by_url


def cron():
    def save_for_each_fb_page(page, cat_name):
        data = {}
        for i in range(1, DATA_MINING_PAGE_DEPTH):
            if i is 1:
                data = get_data_by_page_name(page=page)
            else:
                try:
                    """
                    using try, not data.get()
                    for raising error and
                    returning from the loop
                    """
                    data = get_data_by_page_name(direct_url=data['paging']['next'])
                except:
                    return
            data['data'] = data['data'][:TOP_POST_NUMBER]
            d = data['data']
            
            save_fb_scrapper_all_img_by_url(
                img_url_list=get_keyed_data_as_list(d, 'full_picture'),
                category_name=cat_name,
                img_details={
                    'id': get_keyed_data_as_list(d, 'id'),
                    # 'shares': [x.get('shares')['count'] for x in d],
                    'shares': [x.get('shares')['count'] if x.get('shares') else 0 for x in d],
                    'likes': [x.get('reactions').get('summary')['total_count'] if x.get('reactions').get('summary') else 0 for x in d],
                    'score': get_keyed_data_as_list(d, 'score'),
                }
            )
    
    for fb_pg in fb_pages:
        save_for_each_fb_page(
            page=fb_pg,
            cat_name=fb_pages[fb_pg]
        )


def get_keyed_data_as_list(data, key):
    return [x.get(key) if x.get(key) else 0 for x in data]


if __name__ == "__main__":
    cron()
