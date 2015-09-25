from django.shortcuts import render

from django.contrib.auth.models import User, Group, Permission
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView



from .forms import *



# content_type = ContentType.objects.get(app_label='myapp', model='BlogPost')
# permission = Permission.objects.create(codename='can_publish',
#                                        name='Can Publish Posts',
#                                        content_type=content_type)
# user = User.objects.get(username='duke_nukem')
# group = Group.objects.get(name='wizard')
# group.permissions.add(permission)
# user.groups.add(group)

@csrf_exempt
def add_user_in_group(request):
    if request.method == "GET":
        username = request.GET.get('username','')
        group_name = request.GET.get('group','')

        if group_name and username:
            group = Group.objects.get(name=group_name)
            user = User.objects.get(username=username)
            user.groups.add(group)

            return HttpResponse(status=201, mimetype='application/json')
        else:
            return HttpResponse(status=405, mimetype="application/json")
    else:
        return HttpResponse(status=405, mimetype="application/json")


def user_belonging_in_group(request):

    username = request.GET.get('username','')
    group_name = request.GET.get('group','')

    if group_name and username:
        user = User.objects.get(username=username)

        if user.groups.filter(name=group_name).exists() and user.is_staff:
            return HttpResponse("User belongs to that group",status=200, mimetype='application/json')
    else:
        return HttpResponse("User does not belongs to that group",status=401, mimetype='application/json')

def all_users_in_a_group(request):

    group_name = request.GET.get('group','')

    if group_name:
        users_in_group = Group.objects.get(name=group_name).user_set.all()


class ContactView(FormView):
    template_name = 'base.html'
    form_class = GroupForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(ContactView, self).form_valid(form)
    
class GroupCreate(CreateView):
    template_name  = "groups/create.html"
    model = Group
    fields = ['name']

class GroupUpdate(UpdateView):
    model = Group
    fields = ['name']

class GroupDelete(DeleteView):
    model = Group
    success_url = reverse_lazy('author-list')

class GroupDetailView(DetailView):
    template_name = "groups/detail.html"
    model = Group

class GroupListView(ListView):
    template_name = "groups/listview.html"
    model = Group

