from django_cron import CronJobBase, Schedule
from core.settings import FB_PAGE_SCRAP_FOR_CRON as fb_pages
from fb_scrapper.utils import get_data_by_page_name, save_fb_scrapper_all_img_by_url
from fb_scrapper.models import ScrappedData

# 100x value
DATA_MINER_RANGE = 5

# top post for each 100
TOP_POST_NUMBER = 20


class FbScrapperCron(CronJobBase):
    """
    tasks here will added in cron
    
    docs: http://django-cron.readthedocs.io/en/latest/installation.html
    
    to run this cron: ./manage.py runcrons "fbs_cron.cron.FbScrapperCron"
    
    cron command
    */5 * * * *
    source /home/<user>/.bashrc &&
    source /<virtual env>/bin/activate &&
    python /<project directory>/manage.py runcrons > /<somewhere for log>/cronjob.log
    """
    
    # RUN_EVERY_MINS = 120  # every 2 hours
    # schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    
    RUN_AT_TIMES = ['10:00', '18:00', '2:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    
    code = 'my_app.my_cron_job'  # a unique code
    
    def do(self):
        for fb_pg in fb_pages:
            save_for_each_fb_page(
                page=fb_pg,
                cat_name=fb_pages[fb_pg]
            )


def save_for_each_fb_page(page, cat_name):
    data = {}
    for i in range(1, DATA_MINER_RANGE):
        if i is 1:
            data = get_data_by_page_name(page=page)
        else:
            data = get_data_by_page_name(direct_url=data['paging']['next'])
        data['data'] = data['data'][:TOP_POST_NUMBER]
        d = data['data']
    save_fb_scrapper_all_img_by_url(
        img_url_list=get_keyed_data_as_list(d, 'full_picture'),
        category_name=cat_name,
        img_details={
            'id': get_keyed_data_as_list(d, 'id'),
            'shares': [x.get('shares')['count'] for x in d],
            'likes': [x.get('reactions').get('summary')['total_count'] for x in d],
            'score': get_keyed_data_as_list(d, 'score'),
        }
    )
    #print(data['data'])
    #print(get_keyed_data_as_list(data['data'], 'full_picture'))

def get_keyed_data_as_list(data, key):
    return [x[key] for x in data]
