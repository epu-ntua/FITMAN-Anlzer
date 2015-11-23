import urllib2
import json

def get_twitter_settings():
    #TODO: project names are not unique, so id is used, but this id means nothing and there is no way to know it. By default, id=1 will be used for the "master" project
    project_settings_url = "http://localhost:8000/api/project/1/settings"
    response = urllib2.urlopen(project_settings_url)
    response = response.read()
    response = json.loads(response)
    tw_accounts = ""
    tw_keywords = ""
    for setting in response:
        if setting["DataSourceCategory"]=="Twitter":
            tw_accounts = setting["SearchValueCategory"]
        if setting["DataSourceCategory"]=="Keywords":
            tw_keywords = setting["SearchValueCategory"]
    return tw_accounts,tw_keywords

def get_facebook_settings():
    #TODO: project names are not unique, so id is used, but this id means nothing and there is no way to know it. By default, id=1 will be used for the "master" project
    project_settings_url = "http://localhost:8000/api/project/1/settings"
    response = urllib2.urlopen(project_settings_url)
    response = response.read()
    response = json.loads(response)
    fb_pages = ""
    for setting in response:
        if setting["DataSourceCategory"]=="Facebook":
            fb_pages = setting["SearchValueCategory"]
    return fb_pages

