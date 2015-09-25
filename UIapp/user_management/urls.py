from django.conf.urls import patterns, include, url
from .views import *


urlpatterns = patterns('',
                       # url(r'^$', 'UIapp.views.home', name='home'),
                       # url(r'^UIapp/', include('UIapp.foo.urls')),
                       url(r'^add_user_in_group$', add_user_in_group, name='add_user_in_group'),
                       url(r'^user_belonging_in_group$', user_belonging_in_group, name='user_belonging_in_group'),
                       url(r'^all_users_in_a_group$', all_users_in_a_group, name='all_users_in_a_group'),
                       
                       
                        url(r'group/add/$', GroupCreate.as_view(), name='group_add'),
                        url(r'group/(?P<pk>[0-9]+)/$', GroupUpdate.as_view(), name='group_update'),
                        url(r'group/(?P<pk>[0-9]+)/delete/$', GroupDelete.as_view(), name='group_delete'),

                       url(r'^(?P<pk>[-\w]+)/$', GroupDetailView.as_view(), name='group-detail'),
                       url(r'^$', GroupListView.as_view(), name='group-list'),

)



