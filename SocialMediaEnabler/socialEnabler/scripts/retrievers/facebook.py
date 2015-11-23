from facepy import GraphAPI
from couchbase import Couchbase
from facebook_formatter import *
from settings_retriever import get_facebook_settings
import os

def connectToDb():
    #Define Database connection creds
    server = script_settings.cb_server
    port = script_settings.couchbase_port
    admin_password = script_settings.cb_admin_password
    bucket = script_settings.cb_facebook_bucket
    cbucket = Couchbase.connect(host=server,port=port,bucket=bucket,password=admin_password)
    return cbucket


def save_in_db(cbucket, document):
    cbucket.set(document['fbid'], document)
    return document['fbid']


def saveTextInFile(text, filename):
    result_file = open(script_settings.sentimentQ+"files/%s" % filename, "w")
    result_file.write(str(text.encode('utf-8')))
    result_file.close()
    return True

def saveSpanishTextInFile(text, filename):
    result_file = open(script_settings.sentimentQ+"files_spanish/%s" % filename, "w")
    result_file.write(str(text.encode('utf-8')))
    result_file.close()
    return True

def retrieve_project_settings():
    return get_facebook_settings()


if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from processors.processor import process
        from processors.nlpUtils import idlan
        import script_settings
    else:
        from .. import script_settings
        from ..processors.processor import process
        from ..processors.nlpUtils import idlan
    access_token = script_settings.fb_access_token
    graph = GraphAPI(access_token)
    fb_accounts = retrieve_project_settings()
    fb_pages = fb_accounts.split(",")
    post_retrieval_limit = 2
    if not os.path.exists(script_settings.sentimentQ+"files/"):
        os.makedirs(script_settings.sentimentQ+"files/")
    if not os.path.exists(script_settings.sentimentQ+"files_spanish/"):
        os.makedirs(script_settings.sentimentQ+"files_spanish/")
    for fb_page in fb_pages:
        feed = graph.get('/'+fb_page+'?fields=feed.limit('+str(post_retrieval_limit)+').fields(message,from,created_time,comments.filter(toplevel).fields(message,parent,from,id,created_time),object_id,full_picture),name&locale="en_US"')
        page_name = feed['name']
        feed = feed['feed']['data']
        cb_bucket = connectToDb()
        for message in feed:
            try:
                clean_text = process(message['message'])
                lang = idlan(clean_text)
                if lang == 'english':
                    doc_to_store = parse_post_en(page_name, message, clean_text)
                    data_md5 = save_in_db(cb_bucket, doc_to_store)
                    saveTextInFile(doc_to_store['text_no_url'], data_md5)
                elif lang == 'spanish':
                    doc_to_store = parse_post_es(page_name, message, clean_text)
                    data_md5 = save_in_db(cb_bucket, doc_to_store)
                    saveSpanishTextInFile(doc_to_store['text_no_url_es'], data_md5)
                if "comments" in message:
                    comments = message['comments']['data']
                    for comment in comments:
                        clean_text = process(comment['message'])
                        lang = idlan(clean_text)
                        if lang == 'english':
                            doc_to_store = parse_comment_en(page_name, comment, clean_text)
                            data_md5 = save_in_db(cb_bucket, doc_to_store)
                            saveTextInFile(doc_to_store['text_no_url'], data_md5)
                        elif lang == 'spanish':
                            doc_to_store = parse_comment_es(page_name, comment, clean_text)
                            data_md5 = save_in_db(cb_bucket, doc_to_store)
                            saveSpanishTextInFile(doc_to_store['text_no_url_es'], data_md5)
            except KeyError, e:
                print str(e)
                continue

