#general settings
server_ip = ''

#elasticsearch settings
elastic_search_indices = 'anlzer' #comma seperated list, e.g. 'anlzer2,indexTest'

#couchbase settings
couchbase_port = 8091
couchbase_rss_bucket = "rssfeed" #deprecated after GE removal
couchbase_rss_password = ""
couchbase_bucket = "anlzer"
couchbase_password = ""

#svm model files - IF you change these paths, you must also change them inside SocialMediaEnabler/socialEnabler/scripts/script.settings.py
en_model = '/home/anlzer/sentiment/training_english/models/'
es_model = '/home/anlzer/sentiment/training_spanish/models/'

#do not change after this line
elastic_search_path = 'http://'+server_ip+':9200/'+elastic_search_indices+'/_search'
kibana_path='http://'+server_ip+':9200/_plugin/kibana/index.html#/dashboard/elasticsearch/'

