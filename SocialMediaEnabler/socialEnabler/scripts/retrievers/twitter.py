import json
import hashlib
import time
import datetime
import tweepy
from couchbase import Couchbase
from tweepy.utils import import_simplejson
from twitter_formatter import fix_json_es, fix_json_en
from settings_retriever import get_twitter_settings
import os

def log_msg(filepath,text):
    with open(filepath, "a") as myfile:
        myfile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        myfile.write(text + "\n")

def write_text_to_file(filepath,filename,text):
    result_file = open(filepath+"%s" % filename, "w")
    result_file.write(str(text.encode('utf-8')))
    result_file.close()

#Define Twitter credentials
def set_credentials():
    consumer_key = script_settings.consumer_key
    consumer_secret = script_settings.consumer_secret
    access_token_key = script_settings.access_token_key
    access_token_secret = script_settings.access_token_secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    return auth

#Define Couchbase connection creds and connect to bucket
def get_Couchbase_bucket():
    server = script_settings.cb_server
    port = script_settings.couchbase_port
    admin_username = script_settings.cb_admin_username
    admin_password = script_settings.cb_admin_password
    bucket = script_settings.cb_twitter_bucket
    cbucket = Couchbase.connect(host=server,port=port,bucket=bucket,password=admin_password)
    return cbucket

def set_accounts_from_terms(auth, tw_accounts):
    tw_accounts = tw_accounts.replace("@","")
    inner_accounts_list = tw_accounts.split(",")
    api = tweepy.API(auth)
    results = api.lookup_users(screen_names=inner_accounts_list)
    accounts = []
    for result in results:
        accounts.append(str(result.id))
    return accounts

def get_retrieval_settings():
    return get_twitter_settings()

def settings_changed(configuration,old_configuration):
    if not configuration[0]==old_configuration[0]:
        return True
    if not configuration[1]==old_configuration[1]:
        return True
    return False


class StreamListener(tweepy.StreamListener):
    json = import_simplejson()
    def on_status(self, tweet):
        pass
    def on_timeout(self):
        log_msg("twitterLog.txt","***timeout:sleeping for a minute***")
        time.sleep(60)
        return True  #don't kill the stream

    def on_error(self, status_code):
        log_msg("twitterLog.txt","-----error----" + str(status_code))
        return True  #don't kill the stream

    def on_data(self, data):
        if data[0].isdigit():
            pass
        else:
            data_md5 = hashlib.md5(json.dumps(data, sort_keys=True)).hexdigest()
            json_tweet = json.loads(data)
            try:
                if "text" in json_tweet:
                    text = json_tweet["text"]
                    if "lang" in json_tweet:
                        clean_text = process(text)
                        language = json_tweet["lang"]
                        if language == 'en':
                            if not is_swearing_en(clean_text):
                                json_to_keep = fix_json_en(json_tweet, clean_text)
                                cbucket.set(data_md5,json_to_keep)
                                write_text_to_file(script_settings.sentimentQ+"files/",data_md5,clean_text)

                        elif language == 'es':
                            if not is_swearing_es(clean_text):
                                json_to_keep = fix_json_es(json_tweet, clean_text)
                                cbucket.set(data_md5,json_to_keep)
                                write_text_to_file(script_settings.sentimentQ+"files_spanish/",data_md5,clean_text)
            except Exception,e:
                print e


if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from processors.processor_english import is_swearing_en
        from processors.processor_spanish import is_swearing_es
        from processors.processor import process
        import script_settings
    else:
        from .. import script_settings
        from ..processors.processor_english import is_swearing_en
        from ..processors.processor_spanish import is_swearing_es
        from ..processors.processor import process
    auth1 = set_credentials()
    cbucket = get_Couchbase_bucket()
    l = StreamListener()
    streamer = tweepy.Stream(auth=auth1, listener=l, timeout=3000)
    if not os.path.exists(script_settings.sentimentQ+"files/"):
        os.makedirs(script_settings.sentimentQ+"files/")
    if not os.path.exists(script_settings.sentimentQ+"files_spanish/"):
        os.makedirs(script_settings.sentimentQ+"files_spanish/")
    while True:
        if streamer.running:
            new_configuration = get_retrieval_settings()
            if not settings_changed(new_configuration,configuration):
                pass
            else:
                tw_accounts = new_configuration[0]
                tw_terms = new_configuration[1]
                filterTerms = tw_terms.split(",")
                followAccounts = set_accounts_from_terms(auth1, tw_accounts)
                streamer.disconnect()
                time.sleep(60)
                streamer.filter(follow = followAccounts , track = filterTerms, async=True)
        else:
            configuration = get_retrieval_settings()
            tw_accounts = configuration[0]
            tw_terms = configuration[1]
            followAccounts = set_accounts_from_terms(auth1, tw_accounts)
            filterTerms = tw_terms.split(",")
            streamer.filter(follow=followAccounts, track=filterTerms, async=True)
        time.sleep(600)
