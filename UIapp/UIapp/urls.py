from django.conf.urls import patterns, include, url

from django.contrib import admin
import views
import settings

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'UIapp.views.home', name='home'),
                       # url(r'^UIapp/', include('UIapp.foo.urls')),

                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', views.welcome, name='welcome'),
                       url(r'^welcome$', views.welcome, name='welcome'),
                       url(r'^logout', views.logout_view, name='logout'),
                       url(r'^signup', views.signup, name='signup'),
                       url(r'^welcome-account', views.welcome_account, name='welcome-account'),
                       url(r'^welcome-train', views.welcome_train, name='welcome-train'),
                       url(r'^welcome-categories', views.welcome_categories, name='welcome-categories'),
                       url(r'^welcome-report', views.welcome_report, name='welcome_report'),
                       url(r'^create_query$', views.create_query, name='create_query'),
                       url(r'^dashboard$', views.home, name='home'),
                       url(r'^queries/(\d+)$', views.results, name='results'),
                       url(r'^query/delete/(\d+)$', views.results_delete, name='results_delete'),
                       url(r'^results-update', views.results_update, name='results-update'),
                       url(r'^search', views.search, name='search'),
                       url(r'^settings', views.settings, name='search'),
                       url(r'^train', views.train, name='train'),
                       url(r'^about', views.about, name='about'),
                       url(r'^contact', views.contact, name='contact'),
                       url(r'^socialaccounts', views.validate_social_accounts, name='validate_social_accounts'),
                       # Password Reset
                       #url(r'^password_reset', include('password_reset.urls')),
                       url(r'user_based_sentiment',views.user_based_sentiment,name='user_based_sentiment'),
                       url(r'^download-csv', views.download_csv, name='results-update'),
                       (r'^s/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': settings.STATIC_DOC_ROOT}),


                       (r'^accounts/', include('allauth.urls')),

                       (r'^groups/', include('user_management.urls')),

                       (r'^api/', include('api.urls')),
)



