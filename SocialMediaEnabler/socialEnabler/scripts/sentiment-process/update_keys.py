import os
import time
import sys
from applier_english import applier
from CBConnectorBucket import connector

def update(key,result):
    try:
        cb = connector().cbucket
        document = cb.get(key)
        document.value["senti_tag"] = result
        cb.set(document.key, document.value)
    except:
        return False
    return True


if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        import script_settings
    else:
        from .. import script_settings
    path = script_settings.sentimentQ + '/files/'
    while True:
        try:
            for filename in os.listdir(path):
                with open(path+filename, 'r') as f:
                    line = f.read()
                    line = line.rstrip()
                    result = applier(line,script_settings.en_model)
                    allok = update(filename,result)
                    if not allok:
                        continue
                filen = path+filename
                os.remove(filen)
            print "going to sleep"
            time.sleep(900)
            print "awake!!!"
        except Exception, e:
            print "oups!"
            print e
            print "Unexpected error:", sys.exc_info()[0]
            time.sleep(900)
#            pass
