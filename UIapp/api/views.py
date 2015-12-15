import json
import urllib2

from django.http import HttpResponse
from django.contrib.auth.models import User, Group

from UIapp.models import Project, Query, Category_value, Query_languages, Query_properties
from UIapp.training.train_english import train_en, retrieve_file_en
from UIapp.training.train_spanish import train_sp, retrieve_file_sp
from UIapp.queryHandlers import run_query_through_api
from UIapp import configurations
from UIapp.queryHandlers import parse_query_for_sentiments
import csv
from results import paged_results
# from django.shortcuts import resolve_url
# from django.contrib.auth.views import password_reset
from django.views.decorators.csrf import csrf_exempt



def group_user(request, group_id):
    if request.method == 'GET':
        # project_id = request.GET.get('requestID','')
        group = Group.objects.get(id=group_id)
        if group:
            users = group.user_set.all()
            results = []
            for user in users:
                current_user = {}
                current_user["username"] = user.username
                current_user["url"] = str(request.get_host()) + "/api/user/" + str(user.id)
                results.append(current_user)
            return HttpResponse(json.dumps(results), status=200, content_type='application/json')
        else:
            return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)


def group_user_handle(request, group_id, user_id):
    if request.method == 'GET':
        # project_id = request.GET.get('requestID','')
        group = Group.objects.get(id=group_id)
        user = User.objects.get(id=user_id)
        if group:
            return HttpResponse(status=200, content_type='application/json')
        else:
            return HttpResponse(status=204, content_type='application/json')


def group_user_handle_privileges(request, group_id, user_id):
    if request.method == 'GET':
        # project_id = request.GET.get('requestID','')
        group = Group.objects.get(id=group_id)
        user = User.objects.get(id=user_id)
        if group and user:
            return HttpResponse(json.dumps({"privileges": user.is_staff}), status=200, content_type='application/json')
        else:
            return HttpResponse(status=204, content_type='application/json')


def project_train(request, project_id):
    if request.method == 'GET':
        # project_id = request.GET.get('requestID','')
        project = Project.objects.get(id=project_id)
        # if project:
        #     lan = request.GET.get("lan", "")
        #     if lan == "es":
        #         response = retrieve_file_sp("happy")
        #     elif lan == "en":
        #         response = retrieve_file_en()
        #     else:
        #         response = "You have not selected a valid language. Currently we only support en:english and es:spanish!"
        #         return HttpResponse(json.dumps(response), status=200, content_type='application/json')
        #     return HttpResponse(json.dumps(response), status=200, content_type='html/text')
        # else:
        #     return HttpResponse(status=204, content_type='application/json')
        lan = request.GET.get("lan", "")
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
    elif request.method == 'POST':  # If the form has been submitted...
        lan = request.POST.get("lan", "")
        file = request.FILES['file']
        response = ""
        if file.content_type == 'text/csv':
            if lan == "es":
                try:
                    train_sp(file,configurations.es_model)
                    response = 'System training was completed successfully.'
                    status = 200
                except Exception,e:
                    response = 'The training service is unavailable. Please try again later or contact the system administrator. Error code #1.'
                    status = 500
            else:
                try:
                    train_en(file,configurations.en_model)
                    response =  'System training was completed successfully.'
                    status = 200
                except Exception,e:
                    response =  'The training service is unavailable. Please try again later or contact the system administrator. Error code #2.'
                    status = 500
            return HttpResponse(json.dumps(response), status=status)  # Redirect after POST
        else:
            response =  'Invalid file type. Only text/csv is accepted.'
            status = 500
            return HttpResponse(json.dumps(response), status=status)

    elif request.method == 'PATCH':
        response = "We are currently working on that!"
        return HttpResponse(json.dumps(response), status=200, content_type='application/json')
    else:
        return HttpResponse(status=405, content_type='application/json')


def project_status(request, project_id):
    # TODO missing functionality here
    if request.method == 'GET':
        project = Project.objects.get(id=project_id)
        if project:
            response = "We are working to bring advanced stats and status details about your project. " \
                       "Your preference has already been sent to the admins!"
            return HttpResponse(json.dumps(response), status=200, content_type='application/json')
        else:
            return HttpResponse(status=204, content_type='application/json')
    else:
        return HttpResponse(status=405, content_type='application/json')


def project_group(request, project_id):
    if request.method == 'GET':
        project = Project.objects.get(id=project_id)
        if project:
            group = Group.objects.get(name=project.name)
            response = {
                "url": str(request.get_host()) + "/api/group/" + str(group.id),
                "name": group.name
            }
            return HttpResponse(json.dumps(response), status=200, content_type='application/json')
        else:
            return HttpResponse(status=204, content_type='application/json')

    else:
        return HttpResponse(status=405, content_type='application/json')


def project_stream(request, project_id):
    # TODO missing functionality here
    if request.method == 'GET':
        project = Project.objects.get(id=project_id)
        if project:
            response = "Streaming is not yet supported for this project. Your preference has already been sent to the admins!"
            return HttpResponse(json.dumps(response), status=200, content_type='application/json')
        else:
            return HttpResponse(status=204, content_type='application/json')

    else:
        return HttpResponse(status=405, content_type='application/json')

@csrf_exempt
def project_reports(request, project_id):
    if request.method == 'GET':
        project = Project.objects.get(id=project_id)
        if project:
            queries = Query.objects.filter(owned_by=project)
            results = []
            for query in queries:
                results.append({
                    "created": str(query.created),
                    "name": query.name,
                    "created_by": {
                        "username": query.created_by.username,
                        "url": str(request.get_host()) + "/api/user/" + str(query.created_by.id)
                    },
                    "venn": query.venn,
                    "url": str(request.get_host()) + "/api/project/" + str(project.id) + "/report/" + str(query.id)
                })
            return HttpResponse(json.dumps(results), status=200, content_type='application/json')
        else:
            return HttpResponse(status=204, content_type='application/json')
    elif request.method == 'POST':
        query = run_query_through_api(request, project_id)
        results = {
                    "results": str(request.get_host()) + "/api/project/" + str(project_id) + "/report/"+str(query)+"/results" ,
                    "url": str(request.get_host()) + "/api/project/" + str(project_id) + "/report/"+str(query)
                }
        return HttpResponse(json.dumps(results),status=201, content_type='application/json')
    else:
        return HttpResponse(status=405, content_type='application/json')

def project_settings(request, project_id):
    if request.method == 'GET':
        project = Project.objects.get(id=project_id)
        if project:
            categories = Category_value.objects.filter(owned_by=project)
            results = []
            for category in categories:
                results.append({
                    "SearchValueCategory": category.value,
                    "project": {
                        "name": category.owned_by.name,
                        "url": str(request.get_host()) + "/api/project/" + str(category.owned_by.id)
                    },
                    "DataSourceCategory": category.category.name,
                    "url": str(request.get_host()) + "/api/project/" + str(project.id) + "/settings/"
                })
            return HttpResponse(json.dumps(results), status=200, content_type='application/json')
        else:
            return HttpResponse(status=204, content_type='application/json')
    else:
        return HttpResponse(status=405, content_type='application/json')



def project_report(request, project_id, report_id):
    if request.method == 'GET':
        project = Project.objects.get(id=project_id)
        query = Query.objects.get(id=report_id)
        if project and query:

            result = {
                "created": str(query.created),
                "name": query.name,
                "created_by": {
                    "username": query.created_by.username,
                    "url": str(request.get_host()) + "/api/user/" + str(query.created_by.id)
                },
                "venn": query.venn
            }

            return HttpResponse(json.dumps(result), status=200, content_type='application/json')
        else:
            return HttpResponse(json.dumps("You should check your project and the report to be correct."),status=204, content_type='application/json')

    elif request.method == 'DELETE':
        project = Project.objects.get(id=project_id)
        query = Query.objects.get(id=report_id)
        if project and query:
            query.delete()
            return HttpResponse(status=200, content_type='application/json')
        else:
            return HttpResponse(json.dumps("You should check your project and the report to be correct."),status=204, content_type='application/json')
    else:
        return HttpResponse(status=405, content_type='application/json')


def project_report_results(request, project_id, report_id):
    if request.method == 'GET':
        project = Project.objects.get(id=project_id)
        query = Query.objects.get(id=report_id)

        if project and query:

            return paged_results(request, query.id)
            # return HttpResponse(json.dumps(result), status=200, content_type='application/json')
        else:
            return HttpResponse(json.dumps("You should check your project and the report to be correct."),status=204, content_type='application/json')

    else:
        return HttpResponse(status=405, content_type='application/json')

    # per week results for number of tweets made in a specific PREDEFINED!!! time period regarding a specific topic (topic from list of preexisting topics that are based on hashtags)

#TODO fix this
def histogram_report(request, project_id):
    if request.method == 'GET':
        topic = request.GET.get('topic','')
        if (topic == "api") or (topic == "apis"):
            topic_query_part = "\"doc.entities.hashtags.text:apis OR doc.entities.hashtags.text:api\""
        else:
            topic_query_part = "\"doc.entities.hashtags.text:"+topic+"\""
        query = '{ "facets": { "20": { "date_histogram": { "field": "doc.created_at", "interval": "1w" }, "global": true, "facet_filter": { "fquery": { "query": { "filtered": { "query": { "query_string": { "query": '+topic_query_part+' } }, "filter": { "bool": { "must": [ { "range": { "doc.created_at": { "from": 1430120737063, "to": 1436179293269 } } }, { "terms": { "_type": [ "couchbaseDocument" ] } } ], "must_not": [ { "fquery": { "query": { "query_string": { "query": "doc.entities.hashtags.text:awesomeness" } }, "_cache": true } }, { "fquery": { "query": { "query_string": { "query": "doc.entities.hashtags.text:ub40" } }, "_cache": true } } ] } } } } } } } }, "size": 0}'
        project_settings_url = "http://localhost:9200/futurenterprise/_search?pretty"
        response = urllib2.urlopen(project_settings_url,query)
        response = str(response.read())
        return HttpResponse(response,status=200, content_type='application/json')
    else:
        return HttpResponse(status=405, content_type='application/json')


