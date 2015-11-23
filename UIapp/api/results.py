import datetime
import time

from django.http import Http404, HttpResponse

from UIapp.models import Results
from UIapp.queryHandlers import *

import re
from collections import Counter


def paged_results(request, query_id):
        reponseToPresent = []
        categories_counter = []
        positive_counter = 0
        negative_counter = 0
        neutral_counter = 0
        try:
            ## Must store the response, if there is no response, otherwise return the stored one.
            ## IF NOT STORED
            query = Query.objects.get(id=query_id)
            query_params = Query_properties.objects.filter(query=query)
            results = Results.objects.filter(query=query)
            # run for all categories
            list_properties = get_query_properties(query)
            properties = list_properties["Properties"]  # all the available properties, e.g. keywords, twitter, facebook
            # print "properties: %s" %properties
            phrases = list_properties["Phrases"]
            # print "phrases: %s" %phrases
            keywords = list_properties["Keywords"]
            # print "keywords: %s" %keywords
            twitter_usernames = list_properties["Twitter"]
            facebook_pages = list_properties["Facebook"]
            query_properties = ''  # This is the string that forms the properties query (query_string)
            phrase_properties = ''  # This is the string that forms the phrase query (match_phrase)'
            twitter_properties = ''
            facebook_properties = ''

            ## Run the query or bring the results from the Database
            if results:  # bring it from the database
                response = results.__getitem__(0).results
                response = json.loads(response)
            else:  # make a new query
                lang = Query_languages.objects.get(query=query_id)

                #####
                # Get all the properties, keywords, phrases, twitter usernames
                #####
                for kwrd in keywords.keys():
                    temp = ''
                    for keyword_prop in keywords[kwrd]:
                        temp += "%s," % keyword_prop
                    if query.venn == 'OR':
                        query_properties += '%s,' % remove_comma_at_the_end(temp)
                    else:
                        query_properties += '+(%s)' % remove_comma_at_the_end(temp)
                query_properties = query_properties.replace('+()', '')  # Remove any empty keyword
                query_properties = remove_comma_at_the_end(query_properties)

                if query_properties != '':  # if empty list, no properties, no query string, go to phrases
                    if lang:
                        if lang.language == "es":
                            query_properties = '{"query_string":{"query":"%s","fields":["%s"]}}' % (
                                query_properties, "text_no_url_es")
                        elif lang.language == "en":
                            query_properties = '{"query_string":{"query":"%s","fields":["%s"]}}' % (
                                query_properties, "text_no_url")
                        else:
                            query_properties = '{"query_string":{"query":"%s","fields":["%s","%s"]}}' % (
                                query_properties, "text_no_url", "text_no_url_es")
                    else:
                        query_properties = '{"query_string":{"query":"%s","fields":["%s"]}}' % (
                            query_properties, "text_no_url")

                # Create the phrase query
                for phrase_list in phrases.keys():
                    for phrase in phrases[phrase_list]:
                        if lang:
                            if lang.language == "es":
                                phrase_properties += '{"match_phrase":{"doc.text_no_url_es":"%s"}},' % phrase

                            elif lang.language == "en":
                                phrase_properties += '{"match_phrase":{"doc.text_no_url":"%s"}},' % phrase
                            else:
                                phrase_properties += '{"match_phrase":{"doc.text_no_url":"%s"}},{"match_phrase":{"doc.text_no_url_es":"%s"}},' % (
                                    phrase, phrase)
                        else:
                            phrase_properties += '{"match_phrase":{"doc.text_no_url":"%s"}},' % phrase
                phrase_properties = remove_comma_at_the_end(phrase_properties)

                for twitter_username in twitter_usernames:
                    twitter_properties += '{"match_phrase_prefix" : { "doc.user_screen_name":"twitter:%s" }},' % twitter_username.replace(
                        " ", "").replace("@", "")
                twitter_properties = remove_comma_at_the_end(twitter_properties)

                for facebook_page in facebook_pages:
                    facebook_properties += '{"match_phrase_prefix" : { "doc.user_screen_name":"facebook:%s" }},' % facebook_page.replace(
                        " ", "")
                facebook_properties = remove_comma_at_the_end(facebook_properties)

                ###
                # query constructor
                ###
                query_all = ''
                if (query_properties != ''):
                    query_all += '%s,' % query_properties
                if (phrase_properties != ''):
                    query_all += '%s,' % phrase_properties
                if (twitter_properties != ''):
                    query_all += '%s,' % twitter_properties
                if (facebook_properties != ''):
                    query_all += '%s,' % facebook_properties
                query_all = remove_comma_at_the_end(query_all)

                query_all = '{"query":{"filtered":{"query":{"bool":{"should":[%s],"minimum_should_match" : 1}},"filter":{"bool":{"must":[{"range":{"doc.created_at":{"from":"%s","to":"%s"}}}],"_cache":true}}}},"from":0,"size":10000, "sort":["_score"]}' % (
                    query_all,
                    int(time.mktime(query.from_date.timetuple()) * 1000),
                    int(time.mktime(query.to_date.timetuple()) * 1000))

                print query_all
                response = parse_query_for_sentiments(query_all)
                newResponse = Results(query=query, results=json.dumps(response), updated=datetime.now())
                newResponse.save()

            ## count the occurrences of keywords in in response
            for property in properties.keys():
                word_counter = []
                r = re.compile("|".join(r"\b%s\b" % w.lower() for w in properties[property].split(",")), re.I)
                # temporary solution to double counting...
                number = Counter(re.findall(r, ""))
                for message in response:
                    # dict_you_want = { "text": message["_source"]["doc"]["text"] }
                    # print dict_you_want
                    number = number + Counter(
                        re.findall(r, (message["_source"]["doc"]["text"]).lower().replace("@", " ").replace("#", " ")))
                # for lala in properties[property].split(","):
                #                   print number[lala]
                #                   print lala
                for phrase in properties[property].split(","):
                    #                   number = json.dumps(response).count(phrase)

                    text = '{"name":"%s","times":%i, "sentiment":%i, "positive":%i, "negative":%i, "neutral":%i}' % (
                        phrase.lower(), number[phrase.lower()], 0, 0, 0, 0)
                    # print text
                    word_counter.append(json.loads(text))
                text = {}
                text["category"] = property
                text["properties"] = word_counter
                categories_counter.append(text)

            for message in response:
                doc_text = message["_source"]["doc"]["text"]
                if message["_source"]["doc"]["senti_tag"] == "positive":
                    # for pie diagram metrics
                    positive_counter += 1
                elif message["_source"]["doc"]["senti_tag"] == "negative":
                    # for pie diagram metrics
                    negative_counter += 1
                elif message["_source"]["doc"]["senti_tag"] == "neutral":
                    neutral_counter += 1
                    # if message["_score"] > 0.05:
                if True:
                    reponseToPresent.append(message["_source"])
                    ##print "Just Added: %s" %message["_source"]["doc"]
                    try:
                        for category in categories_counter:
                            r2 = re.compile("|".join(r"\b%s\b" % w["name"].lower() for w in category["properties"]),
                                            re.I)
                            number2 = Counter(re.findall(r2, (
                                json.dumps(message["_source"]["doc"]["text"])).lower().replace("@", " ").replace("#",
                                                                                                                 " ")))
                            if True:
                                for property in category["properties"]:
                                    if message["_source"]["doc"]["senti_tag"] == "positive":
                                        if (number2[property["name"].lower()]) > 0:
                                            property["sentiment"] = property["sentiment"] + 1
                                            property["positive"] = property["positive"] + 1
                                    elif message["_source"]["doc"]["senti_tag"] == "negative":
                                        if (number2[property["name"].lower()]) > 0:
                                            property["sentiment"] = int(property["sentiment"]) - 1
                                            property["negative"] = property["negative"] + 1
                                    elif message["_source"]["doc"]["senti_tag"] == "neutral":
                                        if (number2[property["name"].lower()]) > 0:
                                            property["neutral"] = property["neutral"] + 1
                    except:
                        continue


        except ValueError:
            # print ValueError.message
            raise Http404()

        return HttpResponse(json.dumps(
            {
                # "response": reponseToPresent,
              "positive": positive_counter,
             "negative": negative_counter, "neutral": neutral_counter,
             "categories": categories_counter}

        ), status=200, content_type='application/json')

