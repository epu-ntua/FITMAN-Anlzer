from django.conf.urls import patterns
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers

import views
import viewSets

router = routers.DefaultRouter()
router.register(r'user', viewSets.UserViewSet)
router.register(r'groups', viewSets.GroupViewSet)
router.register(r'project', viewSets.ProjectViewSet)
router.register(r'team', viewSets.TeamViewSet)


admin.autodiscover()

urlpatterns = patterns('',

                       url(r'^', include(router.urls)),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

                       # Group Urls
                       url(r'^group/(\d+)/user$', views.group_user, name='group users'),
                       url(r'^group/(\d+)/user/(\d+)$', views.group_user_handle, name='group users handle'),
                       url(r'^group/(\d+)/user/(\d+)/privileges$', views.group_user_handle_privileges,
                           name='group users handle privileges'),

                       # Project Urls
                       url(r'^project/(\d+)/train$', views.project_train, name='project results'),
                       url(r'^project/(\d+)/status$', views.project_status, name='project status'),
                       url(r'^project/(\d+)/group$', views.project_group, name='project group'),
                       url(r'^project/(\d+)/settings$', views.project_settings, name='project settings'),
                       url(r'^project/(\d+)/stream$', views.project_stream, name='project stream results'),
                       url(r'^project/(\d+)/report$', views.project_reports, name='project reports'),
                       url(r'^project/(\d+)/report/histogram$', views.histogram_report, name='project weekly histogram per topic'),
                       url(r'^project/(\d+)/report/(\d+)$', views.project_report, name='project specific report'),
                       url(r'^project/(\d+)/report/(\d+)/results$', views.project_report_results,
                           name='project results for a report'),

                       )
