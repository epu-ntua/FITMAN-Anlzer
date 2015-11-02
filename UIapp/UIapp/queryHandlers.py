from models import Category, Project, Query, Query_properties,Query_languages
from django.utils import timezone
from dateutil import parser
import urllib2
import configurations
import json

# create a query
def run_query (request):
    user = request.user
    project = Project.objects.get(created_by=user)
    query_name = request.POST.get("query_name", "")
    from_date = request.POST.get("datepicker_from", "")
    to_date = request.POST.get("datepicker_to", "")
    language = request.POST.get("lan", "")
    query = Query(name=query_name, venn=request.POST.get("query_logic", ""), from_date=parser.parse(from_date), to_date=parser.parse(to_date),
                  created=timezone.now(), created_by=user, owned_by=project)
    query.save()
    keywords = request.POST.get("keywords", "")
    category = Category.objects.get(name="Keywords")
    query_property = Query_properties(query=query, category=category, properties=keywords)
    query_property.save()
    twitter = request.POST.get("twitter", "")
    category = Category.objects.get(name="Twitter")
    query_property = Query_properties(query=query, category=category, properties=twitter)
    query_property.save()
    facebook = request.POST.get("facebook", "")
    category = Category.objects.get(name="Facebook")
    query_property = Query_properties(query=query, category=category, properties=facebook)
    query_property.save()
    brands = request.POST.get("brands", "")
    try:
        category = Category.objects.filter(name="brands")
    except ValueError:
        print ValueError.message
    if category.__len__(): #exists already the category
        category = category[0]
    ## otherwise create the category
    else:
        #print "is empty"
        category = Category(name="brands")
        category.save()
    query_property = Query_properties(query=query, category=category, properties=brands)
    query_property.save()
    query_lan=Query_languages(query=query,language=language)
    query_lan.save()

    ##handle dynamic properties
    i = 0;
    prop_value = "prop-value-%s" % i
    prop_name = "prop-name-%s" % i
    while request.POST.get(prop_value, ""):
        property_name = request.POST.get(prop_name, "")
        property_value = request.POST.get(prop_value, "")
        try:
            ## try to find if the category already exists - in lowercase
            category = Category.objects.filter(name=(str(property_name).lower()))
        except ValueError:
            #print ValueError.message
            continue

        if category.__len__(): #exists already the category
            category = category[0]
        ## otherwise create the category
        else:
            category = Category(name=str(property_name).lower())
            category.save()
            ## end store the properties in the category
        query_property = Query_properties(query=query, category=category, properties=property_value)
        query_property.save()

        i += 1
        prop_value = "prop-value-%s" % i
        prop_name = "prop-name-%s" % i

    return query.id

# Get all the properties for a query
# to show them in the table, in the home dashboard
def get_query_properties(query):
    query_properties = Query_properties.objects.filter(query=query)
    keywords={}
    phrases={}
    properties = {}
    result={}
    result["Twitter"]=[]
    result["Facebook"]=[]
    for query_property in query_properties:
            if str((query_property.properties).encode('utf-8')) is "":
                continue
            else:
                phrases[str(query_property.category.name)]=[]
                properties[str(query_property.category.name)] = str((query_property.properties).encode('utf-8'))
                param_list=str(query_property.properties.encode('utf-8')).split(',')
                temp=[]
                for param in param_list:
                    temp.append(param)
                for param in temp:
                    words=param.split()
                    if words.__len__()>1:
                        phrases[str((query_property.category.name).encode('utf-8'))].append(param)
                        param_list.remove(param)
                keywords[str(query_property.category.name.encode('utf-8'))]=param_list
                if str(query_property.category.name.encode('utf-8'))=="Twitter":
                    result["Twitter"]=param_list
                elif str(query_property.category.name.encode('utf-8'))=="Facebook":
                    result["Facebook"]=param_list
    result["Properties"]=properties #The name of the property, e.g. Twitter, Facebook, keywords etc.
    result["Keywords"]=keywords #have keywords per properties category, without phrases
    result["Phrases"]=phrases #have phrases per properties category
    return result


def parse_query_for_sentiments(query):
    response = urllib2.urlopen(
        configurations.elastic_search_path,
        query
    )
    response = response.read()
    response = json.loads(response)["hits"]["hits"]
    return response

# def update_twitter_connector(username, project, twitter_properties):
#     twitter_properties='storeTWaccounts?id=%s_%s&keywords=%s'%(urllib.quote(str(username)),urllib.quote(str(project)), urllib.quote(twitter_properties))
#     #print twitter_properties
#     path="%s%s" %(configurations.twitter_connector,twitter_properties)
#     try:
#         response = urllib2.urlopen(path) ## response = urllib2.urlopen('http://google.com',timeout = 0.001)
#     except urllib2.URLError as err:
#         print('error connecting on twitter settings')
#         return 0
#         # urllib2.URLError: <urlopen error timed out>
#     #response = response.read()
#     #print response
#     return 1

# def update_project_connector(username, project, project_properties):
#     project_properties='storeKeywords?id=%s_%s&keywords=%s'%(urllib.quote(str(username)),urllib.quote(str(project)), urllib.quote(project_properties))
#     #print twitter_properties
#     path="%s%s" %(configurations.twitter_connector,project_properties)
#     try:
#         response = urllib2.urlopen(path)
#     except urllib2.URLError as err:
#         print('error connecting on Keywords settings')
#         return 0
#     #response = response.read()
#     #print response
#     return 1

# def update_facebook_connector(username, project, facebook_properties):
#     facebook_properties='storeFBaccounts?id=%s_%s&keywords=%s'%(urllib.quote(str(username)),urllib.quote(str(project)), urllib.quote(facebook_properties))
#     #print facebook_properties
#     path="%s%s" %(configurations.facebook_connector,facebook_properties)
#     try:
#         response = urllib2.urlopen(path)
#     except urllib2.URLError as err:
#         print('error connecting on Facebook settings')
#         return 0
#     return 1

def remove_comma_at_the_end (expression):
    if len(expression) > 0:
        if expression[-1:] == ",":
            expression = expression[:-1]
    return expression

def remove_plus_in_the_beginning (expression):
    if len(expression) > 0:
        if expression[:1] == "+":
            expression = expression[1:]
    return expression
