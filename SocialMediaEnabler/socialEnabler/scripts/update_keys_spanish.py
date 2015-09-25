import os
import errno
import json
import time
import urllib2
import sys
import script_settings

from CBConnectorBucket import connector


def silentremove(filename):
    print "removing file:"+filename
    try:
        os.remove(filename)
        print "file removed"
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occured


def update(key, value, conpos, conneg):
    print "in update"
    cb = connector().cbucket
#    print "connected"
    if needs_update(conpos,conneg): 
        try:
            print "entry needs update"
            document = cb.get(key)
            document.value["senti_tag"] = value
            cb.set(document.key, document.value)
            print "entry was updated"
        except:
            return False
    print "now exiting update"
    return True

# define when neutral sentiment should change to positive/negative based on confidence from rapidminer	
def needs_update(x,y):
    if abs(x-y)<0.1:
        return False
    return True		

# parse file
def parse(data):
    print "entered parse"
    file_name = data['"metadata_file"']
#    print "1"
    file_name = file_name.replace('"', '')
#    print "2"
    file_path = data['"metadata_path"']
#    print "3"
    file_path = file_path.replace('"','')
#    print "4"
    result = data['"prediction(att2)"']
#    print "5"
    result = result.replace('"', '')
#    print "6"
    confidence_pos = data['"confidence(positive)"']
#    print "7"
    confidence_neg = data['"confidence(negative)"']
#    print "8"
    if update(file_name, result, confidence_pos, confidence_neg):
        print "will call silentremove"
        silentremove(file_path)
        print "silentremove returned"


while True:
    try:
        print "will call readUpdates for spanish docs"
        response = urllib2.urlopen(script_settings.rapidanalytics_path+'readUpdatesSpanish')
        print "Spanish readUpdates done"
#        print response    #careful cannot print empty
        content = response.read()
        print "read ok"
#        print content
        if not content:
            pass
#            print "empty string"
        else:
#            print "okk"
            data = json.loads(content)
#            print data        #careful cannot print empty
            print "will now parse"
            if '"metadata_path"' in data:
                parse(data) #careful!!!when there is only one result in data parse(result) fails
            else:
                for result in data:
#                    print result
                    print "parsing next"
                    parse(result)
        print "gonna sleep"
        time.sleep(900)
#        print "awake!!!"
    except:
        print "oups!"
#        print "Unexpected error:", sys.exc_info()[0]
        time.sleep(900)
#        pass
