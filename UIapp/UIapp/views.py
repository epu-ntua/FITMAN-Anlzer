from django.contrib import messages
from django.template import RequestContext
import urllib2, urllib
import json
import datetime
import time
from queryHandlers import *
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import Group, User
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from initialiaze_repo import initialize
from models import Category, Team, Project, Category_value, Query, Query_properties, Results, Query_languages
# TODO manage the following dependency on future settings
from updateSentimentKeys import multiple_values_update
import csv
import configurations
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
# from django.shortcuts import resolve_url
from django.core.urlresolvers import reverse, resolve
from django.template.response import TemplateResponse
#from django.contrib.auth.views import password_reset
import re
from collections import Counter
import requests
from .utils import user_is_allowed_to_change_the_project
from training.train_english import train_en
from training.train_spanish import train_sp


def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


###
#initial screens
###
def welcome(request):
    if request.user.is_authenticated():
        # Do something for authenticated users.
        #print ('is autenticated')
        return HttpResponseRedirect("/dashboard")  # Redirect after POST

    if request.method == 'POST':  # If the form has been submitted...
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        user = authenticate(username=email, password=password)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(request, user)
                print("User is valid, active and authenticated")
                #set user on session property to read it from results
            else:
                print("The password is valid, but the account has been disabled!")
                return HttpResponseRedirect("/")  # Redirect after POST
        else:
            # the authentication system was unable to verify the username and password
            #print("The username or password were incorrect.")
            return HttpResponseRedirect("/")  # Redirect after POST

        #Check authenticated
        #If  ok
        return HttpResponseRedirect("/dashboard")  # Redirect after POST
        #If not authenticated
        #inform
    else:
        #print RequestContext(request)
        #for development mode only!!
        initialize()
        #print RequestContext(request)
        return render(request, "welcome.html",context_instance=RequestContext(request))


def welcome_account(request):
    if request.method == 'POST':  # If the form has been submitted...
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        user = authenticate(username=email, password=password)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                print("User is valid, active and authenticated")
                #set user on session property to read it from results
            else:
                #print("The password is valid, but the account has been disabled!")
                return HttpResponseRedirect("/")  # Redirect after POST
        else:
            # the authentication system was unable to verify the username and password
            #print("The username or password were incorrect.")
            return HttpResponseRedirect("/")  # Redirect after POST

        #Check authenticated
        #If  ok
        return HttpResponseRedirect("/dashboard")  # Redirect after POST
        #If not authenticated
        #inform
    else:
        #for development mode only!!
        #initialize()
        return render(request, "welcome.html")

    return render_to_response("welcome_account.html")


## step1
def welcome_categories(request):
    #must create project!
    if request.method == 'POST':  # If the form has been submitted...
        #from session
        email = request.session.get("signup-email")
        password = request.session.get("signup-password")
        username = request.session.get("signup-username")
        #from request parameters
        project = request.POST.get("project", "")
        twitter = request.POST.get("twitter", "")
        facebook = request.POST.get("facebook", "")
        hashtags = request.POST.get("hashtags", "")

        accounts = {}
        accounts['twitter'] = twitter
        accounts['facebook'] = facebook

        twitter_properties = ""
        facebook_properties = ""

        if str(project).isspace() or not str(project):  #not a project name
            return render(request, "welcome_categories.html", {"message": 'Project name is required'})
        elif str(project).isspace() or str(twitter).isspace() or str(facebook).isspace() or str(
                hashtags).isspace() or str(hashtags).isspace():  #strings with gaps
            return render(request, "welcome_categories.html", {"message": 'Please remove empty spaces'})
        elif not str(twitter) and not str(facebook) and not str(hashtags):  #empty strings
            return render(request, "welcome_categories.html",
                          {"message": 'Please provide at least one parameter to initialize your project'})
        elif validate_social_accounts(accounts) is not True:
            social_accounts = validate_social_accounts(accounts)

            return render(request, "welcome_categories.html",
                          {"message": 'Not Valid accounts!! You should fix the following accounts: '+', '.join(social_accounts)})
        else:
            #create user
            #create project
            #create properties
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            #print user
            team = Team(name=username, created_by=user)
            team.save()
            current_project = Project(name=project, created_by=user, owned_by=team)
            current_project.save()
            newgroup = Group.objects.create(name=str(project))
            newgroup.save()
            project = current_project
            categoryK = Category.objects.get(name="Keywords")
            categoryT = Category.objects.get(name="Twitter")
            categoryF = Category.objects.get(name="Facebook")
            if twitter:
                Category_value.objects.create(value=twitter, category=categoryT, owned_by=project).save()
                twitter_properties += twitter
            else:
                Category_value.objects.create(value="", category=categoryT, owned_by=project).save()
            if facebook:
                Category_value.objects.create(value=facebook, category=categoryF, owned_by=project).save()
                facebook_properties += facebook
            else:
                Category_value.objects.create(value="", category=categoryF, owned_by=project).save()
            if hashtags:
                Category_value.objects.create(value=hashtags, category=categoryK, owned_by=project).save()
                twitter_properties += ",%s" % hashtags
            else:
                Category_value.objects.create(value="", category=categoryK, owned_by=project).save()
            user2 = authenticate(username=username, password=password)
            if user2 is not None:
                # the password verified for the user
                if user2.is_active:
                    login(request, user2)
                    print("User is valid, active and authenticated")
                    #set user on session property to read it from results
                else:
                    print("The password is valid, but the account has been disabled!")
                    return HttpResponseRedirect("/")  # Redirect after POST
            else:
                # the authentication system was unable to verify the username and password
                #print("The username or password were incorrect.")
                return HttpResponseRedirect("/signup")  # Redirect after POST
        request.session['signup-username'] = ""
        request.session['signup-email'] = ""
        request.session['signup-password'] = ""

        # setup project on twitter keyword connector
        error_message = "no"
        if not update_project_connector(username, project, twitter_properties):
            error_message = "Error connecting to database. Project settings were not stored. Please contact the system administrator. Error code #3."
            messages.add_message(request, messages.ERROR, error_message)
        # setup project on twitter acount connector
        if not update_twitter_connector(username,project,twitter):
            error_message = "Error connecting to database. Project settings were not stored. Please contact the system administrator. Error code #4."
            messages.add_message(request, messages.ERROR, error_message)
        # setup project on fb connector
        if not update_facebook_connector(username, project, facebook_properties):
            error_message = "Error connecting to database. Project settings were not stored. Please contact the system administrator. Error code #5."
            messages.add_message(request, messages.ERROR, error_message)

        if error_message == "no":
            return HttpResponseRedirect("/welcome-train")
        else:
            return HttpResponseRedirect("/welcome-categories")
    else:

        return render(request, 'welcome_categories.html', context_instance=RequestContext(request))


## step 2
def welcome_train(request):
    #we have now user, thus we must authenticate them before train the system to avoid attacks
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")  # Redirect to initial screen

    if request.method == 'POST':  # If the form has been submitted...
        #remove training functionality so early in the process...
        messages.add_message(request, messages.ERROR, 'System training is now performed only through the main menu, after project configuration has successfully been completed.')
        return HttpResponseRedirect("/welcome-train")  #

    else:
        return render(request, 'welcome_train.html',context_instance=RequestContext(request))


## step 3
def welcome_report(request):
    #we have now user, thus we must authenticate them before train the system to avoid attacks
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")  # Redirect to initial screen
    if request.method == 'POST':
        run_query(request)
        return HttpResponseRedirect("/dashboard")  # Redirect after POST

    return render(request, "welcome_report.html")


def index(request):
    return render_to_response("index.html")


###
#Handle authenticaction
###
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    messages.add_message(request, messages.INFO, 'Signout Successful.')
    return HttpResponseRedirect("/welcome")


def signup(request):
    if request.method == 'POST':  # If the form has been submitted...
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")
        if str(username).isspace() or str(email).isspace() or str(password).isspace():  #strings with gaps
            return render(request, "signup.html", {"message": 'Please fill in all the fields'})
        elif not str(username) or not str(email) or not str(password) or not str(password2):  #empty strings
            return render(request, "signup.html", {"message": 'Please fill in all the fields'})
        elif User.objects.filter(username=(str(username).lower())):  #user exists
            return render(request, "signup.html", {"message": 'Choose another username'})
        elif User.objects.filter(username=(str(email).lower())):  # email exists
            return render(request, "signup.html", {"message": 'This email is in use'})
        elif str(password) != str(password2):  #not same password
            return render(request, "signup.html", {"message": 'Wrong password verification'})
        else:
            request.session['signup-username'] = str(username).lower()
            request.session['signup-email'] = str(email).lower()
            request.session['signup-password'] = password

        return HttpResponseRedirect("/welcome-categories")
    else:
        return render(request, 'signup.html')


###
#Landing Page
###
def home(request):
    # get the authenicated user instead
    #teams = Team.objects.filter(created_by=request.user)
    # # to be selected by the user
    # current_team=teams.latest()
    # projects=Project.objects.filter(owned_by=current_team.name, created_by=user.username)

    if request.user.is_authenticated():
        current_project = Project.objects.filter(created_by=request.user).latest("created")
        queries = Query.objects.filter(owned_by=current_project.id)
        list_of_queries = []
        titles = ['Name', 'Keywords', 'Accounts', 'Created by', 'From', 'To', 'Created']
        for query in queries:
            query_response = {}
            query_response['id'] = query.id
            query_response['Name'] = query.name
            query_response['Created_by'] = query.created_by.username
            query_response['From'] = query.from_date.date()
            query_response['To'] = query.to_date.date()
            query_response['Created'] = query.created.date()
            #query_response= "{'id':'%s','Name': '%s'" %(query.id, query.name)
            dynamic_properties = get_query_properties(query)["Properties"]
            if (dynamic_properties.get("Keywords") or dynamic_properties.get("keywords")):
                query_response['Keywords'] = dynamic_properties["Keywords"]
            if (dynamic_properties.get("Twitter") or dynamic_properties.get("twitter")):
                query_response['Usernames'] = dynamic_properties["Twitter"]
            if (dynamic_properties.get("Facebook") or dynamic_properties.get("facebook")):
                query_response['Usernames'] = dynamic_properties["Facebook"]
            ##print "The property name is:%s" % query_response['Keywords']

            # query_properties = Query_properties.objects.filter(query=query)
            # for query_property in query_properties:
            #     #print "The property object is:%s" %query_property.category.name
            #     # a Category that must a appear in the table header
            #     #if query_property.category.name not in titles:
            #         #titles.append("%s" % query_property.category.name)
            #     # add the property name & value to the response
            #     if query_property.category.name=='Keywords':
            #         #query_response += ",'%s':%s"%(query_property.category.name, query_property.properties)
            #         query_response['Keywords']=query_property.properties
            #         #print "The property name is:%s" %query_property.properties
            list_of_queries.append(query_response)
        return render_to_response("home.html", {"headers": titles, "content": list_of_queries})
    else:
        return HttpResponseRedirect("/")


###
#queries
###
def create_query(request):
    if not request.user.is_authenticated():
        # Do something for anonymous users.
        return HttpResponseRedirect("/dashboard")  # Redirect after POST

    if request.method == 'POST':  # If the form has been submitted...
        ##Do not allow users to vote before a timeperiod has passed.
        run_query(request)
        return HttpResponseRedirect("/dashboard")  # Redirect after POST
    else:
        return render(request, 'create_query.html')


def results(request, query_id):
    """
    :param request:
    :param query_id:
    :return: :raise:
    """
    if request.user.is_authenticated():
        reponseToPresent = []
        categories_counter = []
        positive_counter = 0
        negative_counter = 0
        neutral_counter = 0
        try:
            ## Must store the response, if there is no response, otherwise return the stored one.
            ## IF NOT STORED
            query = Query.objects.get(id=query_id, created_by=request.user)
            query_params = Query_properties.objects.filter(query=query)
            results = Results.objects.filter(query=query)
            #run for all categories
            list_properties = get_query_properties(query)
            properties = list_properties["Properties"]  # all the available properties, e.g. keywords, twitter, facebook
            #print "properties: %s" %properties
            phrases = list_properties["Phrases"]
            #print "phrases: %s" %phrases
            keywords = list_properties["Keywords"]
            #print "keywords: %s" %keywords
            twitter_usernames = list_properties["Twitter"]
            facebook_pages = list_properties["Facebook"]
            query_properties = ''  # This is the string that forms the properties query (query_string)
            phrase_properties = ''  # This is the string that forms the phrase query (match_phrase)'
            twitter_properties = ''
            facebook_properties = ''

            ## Run the query or bring the results from the Database
            if results:  #bring it from the database
                response = results.__getitem__(0).results
                response = json.loads(response)
            else:  #make a new query
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
                query_properties = query_properties.replace('+()', '')  #Remove any empty keyword
                query_properties = remove_comma_at_the_end(query_properties)

                if query_properties != '':  #if empty list, no properties, no query string, go to phrases
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
                #query constructor
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
                newResponse = Results(query=query, results=json.dumps(response), updated=datetime.datetime.now())
                newResponse.save()


            ## count the occurrences of keywords in in response
            for property in properties.keys():
                word_counter = []
                r = re.compile("|".join(r"\b%s\b" % w.lower() for w in properties[property].split(",")), re.I)
                # temporary solution to double counting...
                number = Counter(re.findall(r, ""))
                for message in response:
                    #dict_you_want = { "text": message["_source"]["doc"]["text"] }
                    #print dict_you_want
                    number = number + Counter(re.findall(r, (message["_source"]["doc"]["text"]).lower().replace("@", " ").replace("#", " ")))
                #                for lala in properties[property].split(","):
                #                   print number[lala]
                #                   print lala
                for phrase in properties[property].split(","):
                    #                   number = json.dumps(response).count(phrase)

                    text = '{"name":"%s","times":%i, "sentiment":%i, "positive":%i, "negative":%i, "neutral":%i}' % (
                    phrase.lower(), number[phrase.lower()], 0, 0, 0, 0)
                    #print text
                    word_counter.append(json.loads(text))
                text = {}
                text["category"] = property
                text["properties"] = word_counter
                categories_counter.append(text)

            for message in response:
                doc_text = message["_source"]["doc"]["text"]
                if message["_source"]["doc"]["senti_tag"] == "positive":
                    #for pie diagram metrics
                    positive_counter += 1
                elif message["_source"]["doc"]["senti_tag"] == "negative":
                    # for pie diagram metrics
                    negative_counter += 1
                elif message["_source"]["doc"]["senti_tag"] == "neutral":
                    neutral_counter += 1
                    #if message["_score"] > 0.05:
                if True:
                    reponseToPresent.append(message["_source"])
                    ##print "Just Added: %s" %message["_source"]["doc"]
                    try:
                        for category in categories_counter:
                            r2 = re.compile("|".join(r"\b%s\b" % w["name"].lower() for w in category["properties"]),
                                            re.I)
                            number2 = Counter(re.findall(r2, (
                            json.dumps(message["_source"]["doc"]["text"])).lower().replace("@", " ").replace("#", " ")))
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
            #print ValueError.message
            raise Http404()


        return render(request, "results.html",
                      {"query_id": query.id, "query_name": query.name, "query": query_params,
                       "response": reponseToPresent, "positive": positive_counter,
                       "negative": negative_counter, "neutral": neutral_counter,
                       "categories": categories_counter})
    else:
        return HttpResponseRedirect("/")


def results_delete(request, query_id):
    query = Query.objects.get(id=query_id)
    query.delete()
    return HttpResponseRedirect("/dashboard")  # Redirect after update to the page


# TODO:something never works properly here
def results_update(request):
    print "Entering results_update"
    if request.method != 'POST':  # If the form has not been submitted...
        raise Http404('Only POST methods allowed')
    update_bulk = request.POST.get("retrain", "")
    ## send the bulk to the db service
    req = urllib2.Request("http://localhost:8000/user_based_sentiment?sentiment_values=%s" % str(update_bulk))
    resp = urllib2.urlopen(req)
    print resp
    response = resp.read()
    print "stored: %s" %response
    ## delete cashing from results, to get the updated ones from "results" methods
    results_id = request.POST.get("results-id", "")
    query = Query.objects.get(id=results_id)
    results = Results.objects.get(query=query)
    if results:
        results.delete()
    ## redirect to the proper page again
    path = "/queries/%s" % results_id
    print path
    print results_id
    return HttpResponseRedirect(path)  # Redirect after update to the page


###
#Toolbar
###
def search(request):
    return render_to_response("free-search.html", {"kibana": configurations.kibana_path})

def train(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/dashboard")  # Redirect after POST
    if request.method == 'POST':  # If the form has been submitted...
        lan = request.POST.get("lan", "")
        file = request.FILES['file']
        if file.content_type == 'text/csv':
            if lan == "es":
                try:
                    train_sp(file,configurations.es_model)
                    messages.add_message(request, messages.INFO, 'System training was completed successfully.')
                except Exception,e:
                    messages.add_message(request, messages.ERROR, 'The training service is unavailable. Please try again later or contact the system administrator. Error code #1.')
            else:
                try:
                    train_en(file,configurations.en_model)
                    messages.add_message(request, messages.INFO, 'System training was completed successfully.')
                except Exception,e:
                    messages.add_message(request, messages.ERROR, 'The training service is unavailable. Please try again later or contact the system administrator. Error code #2.')
            return HttpResponseRedirect("/training")  # Redirect after POST
        else:
            messages.add_message(request, messages.ERROR, 'Invalid file type. Only text/csv is accepted.')
            return HttpResponseRedirect("/training")  #

    else:
        return render(request, 'training.html',context_instance=RequestContext(request))



def about(request):
    return render_to_response("about.html")


def settings(request):
    if request.user.is_authenticated():
        project = Project.objects.filter(created_by=request.user).latest("created")
        if request.method != 'POST':
            keywords = twitter = facebook = ""
            for project_settings in Category_value.objects.filter(owned_by=project):
                if project_settings.category.name == "Keywords":
                    keywords = project_settings.value
                elif project_settings.category.name == "Twitter":
                    twitter = project_settings.value
                elif project_settings.category.name == "Facebook":
                    facebook = project_settings.value

            return render(request, "settings.html",
                          {"keywords": keywords, "twitter": twitter, "facebook": facebook},context_instance=RequestContext(request))
        else:
            if not user_is_allowed_to_change_the_project(username=request.user.username,group_name=project):
                # TODO send mail to the admins with the preferences
                error_message = "You have no administrative rights to change this project. Please contact the administrator of your project for more privileges. "
                messages.add_message(request, messages.ERROR, error_message)
                keywords = twitter = facebook = ""
                project = Project.objects.filter(created_by=request.user).latest("created")
                for project_settings in Category_value.objects.filter(owned_by=project):
                    if project_settings.category.name == "Keywords":
                        keywords = project_settings.value
                    elif project_settings.category.name == "Twitter":
                        twitter = project_settings.value
                    elif project_settings.category.name == "Facebook":
                        facebook = project_settings.value
                return render(request, "settings.html",
                          {"message":messages,"keywords": keywords, "twitter": twitter, "facebook": facebook},context_instance=RequestContext(request))



            #get properties
            twitter = request.POST.get("twitter", "")
            facebook = request.POST.get("facebook", "")
            keywords = request.POST.get("keywords", "")

            accounts = {}
            accounts['twitter'] = twitter
            accounts['facebook'] = facebook

            if validate_social_accounts(accounts) is not True:
                social_accounts = validate_social_accounts(accounts)
                error_message =  'Not Valid accounts!! You should fix the following accounts: '+', '.join(social_accounts)
                messages.add_message(request, messages.ERROR, error_message)

                return render(request, "settings.html",
                              {"message": error_message},context_instance=RequestContext(request))
            #update twitter
            category = Category.objects.get(name="Twitter")
            if Category_value.objects.filter(owned_by=project, category=category).count() == 0:
                Category_value.objects.create(owned_by=project, category=category, value="").save()
            else:
                category_val = Category_value.objects.get(owned_by=project, category=category)
                category_val.value = twitter
                category_val.save()

            #update facebook
            category = Category.objects.get(name="Facebook")
            if Category_value.objects.filter(owned_by=project, category=category).count() == 0:
                Category_value.objects.create(owned_by=project, category=category, value="").save()
            else:
                category_val = Category_value.objects.get(owned_by=project, category=category)
                category_val.value = facebook
                category_val.save()

            #update keywords
            category = Category.objects.get(name="Keywords")
            if Category_value.objects.filter(owned_by=project, category=category).count() == 0:
                Category_value.objects.create(owned_by=project, category=category, value="").save()
            else:
                category_val = Category_value.objects.get(owned_by=project, category=category)
                category_val.value = keywords
                category_val.save()


            twitter_properties = twitter
            keyword_properties = keywords+","+twitter
            #update twitter connector
            if not update_project_connector(project.owned_by.name, project.name, keyword_properties):
                error_message = "Error connecting to database. Project settings were not stored. Please contact the system administrator. Error code #6."
                messages.add_message(request, messages.ERROR, error_message)
            if not update_twitter_connector(project.owned_by.name, project.name, twitter_properties):
                error_message = "Error connecting to database. Project settings were not stored. Please contact the system administrator. Error code #7."
                messages.add_message(request, messages.ERROR, error_message)
            #update facebook connector
            if not update_facebook_connector(project.owned_by.name, project.name, facebook):
                error_message = "Error connecting to database. Project settings were not stored. Please contact the system administrator. Error code #8."
                messages.add_message(request, messages.ERROR, error_message)

            return render(request, "settings.html",
                          {"keywords": keywords, "twitter": twitter, "facebook": facebook},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")


def contact(request):
    return render_to_response("contact.html")


def user_based_sentiment(request):
    if request.method == 'GET':
        sentiment_values = request.GET.get("sentiment_values", "")
        if sentiment_values:
            print "there are values to be updated"
            print sentiment_values
            sentiment_values = sentiment_values.replace(" ", "")
            sentiment_values = sentiment_values.split(",")

            if '' in sentiment_values:
                sentiment_values.remove('')
            lista = []

            for value in sentiment_values:
                res = value.split(":")
                if "'" in res:
                    continue
                i = 0
                found = False
                while i < len(lista):
                    if res[0] is lista[i]['key']:
                        lista[i]['value'] = res[1]
                        found = True
                    i = i + 1
                if found is False:
                    lista.append({'key': res[0], 'value': res[1]})
            result = multiple_values_update(lista)

            return HttpResponse(status=200, mimetype='application/json')
        else:
            return HttpResponse(status=204, mimetype='application/json')

    else:
        return HttpResponse(status=405)


def download_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    lan = request.GET.get("lan", "")
    #print lan
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="train-sentiment.csv"'
    writer = csv.writer(response)
    if lan == "en":
        training_query = '{"query" : {"filtered" : {"query" : {"bool" : {"should" : [{"query_string" : {"query" : "*"}}]}},"filter" : {"bool" : {"must" : [{"match_all" : {}},{"terms" : {"_type" : ["couchbaseDocument"]}},{"terms" : {"doc.lang" : ["en"]}},{"bool" : {"must" : [{"match_all" : {}}]}}]}}}},"size" : 1000,"sort": [{"doc.created_at": {"order": "desc"}}],"fields" : ["doc.text_no_url","doc.senti_tag"]}'
    else:
        training_query = '{"query" : {"filtered" : {"query" : {"bool" : {"should" : [{"query_string" : {"query" : "*"}}]}},"filter" : {"bool" : {"must" : [{"match_all" : {}},{"terms" : {"_type" : ["couchbaseDocument"]}},{"terms" : {"doc.lang" : ["es"]}},{"bool" : {"must" : [{"match_all" : {}}]}}]}}}},"size" : 1000,"sort": [{"doc.created_at": {"order": "desc"}}],"fields" : ["doc.text_no_url_es","doc.senti_tag"]}'
    parsed = parse_query_for_sentiments(training_query)
    #print parsed
    for message in parsed:
        try:
            if lan == "en":
                writer.writerow([str(message["fields"]["doc.text_no_url"]).replace(",", " ").strip(),
                                 message["fields"]["doc.senti_tag"]])
            else:
                writer.writerow([str(message["fields"]["doc.text_no_url_es"]).replace(",", " ").strip(),
                                 message["fields"]["doc.senti_tag"]])
        except:
            continue
    return response


def validate_social_accounts(accounts):
        # accounts = request.GET.get("accounts", "")
        if accounts:
            facebook_accounts = accounts['facebook']
            twitter_accounts  = accounts['twitter']

            facebook_accounts = facebook_accounts.split(',')
            twitter_accounts = twitter_accounts.split(',')

            twitter_accounts = [w.replace(' ','') for w in twitter_accounts]
            facebook_accounts = [w.replace(' ','') for w in facebook_accounts]


            valid_accounts = {}
            valid_accounts['facebook'] = []
            valid_accounts['twitter'] = []

            not_valid_accounts = []

            for account in facebook_accounts:
                if "facebook.com" in account:
                    if requests.get(account).status_code == 200:
                        valid_accounts['facebook'].append(account)
                    else:
                        not_valid_accounts.append(str(account))
                else:
                    if requests.get("https://www.facebook.com/"+account).status_code == 200:
                        valid_accounts['facebook'].append("https://www.facebook.com/"+account)
                    else:
                        not_valid_accounts.append(str(account))

            for account in twitter_accounts:
                if "twitter.com" in account:
                    if requests.get(account).status_code == 200:
                        valid_accounts['twitter'].append(account)
                    else:
                        not_valid_accounts.append(str(account))
                else:
                    if account[0]=="@":
                        account = account.replace("@","")
                    if requests.get("https://www.twitter.com/"+account).status_code == 200:
                        valid_accounts['twitter'].append("https://www.twitter.com/"+account)
                    else:
                        not_valid_accounts.append(str(account))
            if not_valid_accounts == []:
                return True
            else:
                return not_valid_accounts
        else:
            return False
