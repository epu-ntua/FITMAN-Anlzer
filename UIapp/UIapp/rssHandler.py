from wordCounter import findCommonWords
import json
import urllib2
import configurations
import tempfile
from couchbase import Couchbase

def connectTOdb():
    server = configurations.server_ip
    port = configurations.couchbase_port
    bucket = configurations.couchbase_rss_bucket
    password = configurations.couchbase_rss_password
    cbucket = Couchbase.connect(host=server, port=port, bucket=bucket, password=password)
    return cbucket

def parseRSSresponse(response):
    total_text = " "
    content = json.loads(response)
    positives = 0
    negatives = 0
    neutrals = 0
    cb = connectTOdb()
    print content
    for result in content:
        cb_id = "ge"+result["id"]
        total_text += result["text"]

        try:
            doc = cb.get(cb_id)
            sentiment = doc.value["sentiment"]
            result["sentiment"]=sentiment
            result["gid"]=cb_id
            if sentiment == "positive":
                positives+=1
            elif sentiment == "negative":
                negatives+=1
            else:
                neutrals+=1
        except:
            try:
                sentiment = get_sentiment_prediction(result["text"])
                print sentiment
                json_to_keep = {'sentiment':sentiment}
                cb.set(cb_id,json_to_keep)
                result["sentiment"]= sentiment
                result["gid"]=cb_id
                if sentiment == "positive":
                    positives+=1
                elif sentiment == "negative":
                    negatives+=1
                else:
                    neutrals+=1
            except Exception:
                print Exception.message
    common_words = findCommonWords(total_text)

    return (content,positives,negatives,neutrals,common_words)

def get_sentiment_prediction(text):
    print text
    print "I will invoke rss sentiment analysis process"
    file = tempfile.TemporaryFile()
    try:
        text = text.encode('utf-8').strip()
        file.write(text)
    except Exception as e:
        print str(e)
        print "oups"
    req = urllib2.Request(configurations.rss_sentiment_analysis_path)
    req.add_header('-T', file)
    resp = urllib2.urlopen(req)
    response = resp.read()
    print response
    sentiment = getSentimentValue(response)
    file.close()
    return sentiment

def getSentimentValue(response):
    jresponse = json.loads(response)
    return jresponse["prediction(label)"]



