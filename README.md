# [9moja](http://9moja.com) #

### Versions ###
* python-3
* django-1.11

### Database for first-time: ###
go to project directory/processors/ ,
run _create_db.sh_

### Set up cron: ###

go to project directory/processors/ ,
run _start_cron.sh_

### Options: ###

* core/settings.py
  * `FB_PAGE_SCRAP_FOR_CRON` for cron job facebook scrapping
    * Add page id (from facebook url) / if username set up in page, it can also be used
    * Set a unique name for this page. It'll be used as a category
  * `SOCIAL_AUTH_FACEBOOK_KEY` and `SOCIAL_AUTH_FACEBOOK_SECRET`
    * facebook _app id_ and _secret id_
  * `SOCIAL_AUTH_TWITTER_KEY` and `SOCIAL_AUTH_TWITTER_SECRET`
    * twitter _app id_ and _secret id_
* processors/cron.py
  * `DATA_MINING_PAGE_DEPTH`
    * facebook scrapping can be done for 100 data each time. 
        This value will be set for how many pages data will be scrapped
  * `TOP_POST_NUMBER`
    * facebook top post (according to share and like) number
   
### add cron job task ###
* chmod 755 <project_directory>/processors/start_cron.sh
* open terminal and type `crontab -e`
* add this line at the very bottom `0 */8 * * * <project_directory>/processors/start_cron.sh` (this will run every 8 hours)
* for help, visit: [crontab guru](https://crontab.guru) 