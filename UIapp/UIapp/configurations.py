#general settings
server_ip = ''

#elasticsearch settings
elastic_search_indices = 'anlzer2' #comma seperated list, e.g. 'anlzer2,indexTest'

#couchbase settings
couchbase_port = 8091
couchbase_rss_bucket = "rssfeed" #deprecated after GE removal
couchbase_rss_password = ""
couchbase_bucket = "anlzer"
couchbase_password = ""

#do not change after this line
elastic_search_path = 'http://'+server_ip+':9200/'+elastic_search_indices+'/_search'
kibana_path='http://'+server_ip+':9200/_plugin/kibana/index.html#/dashboard/elasticsearch/'

#svm model files
en_model = '/home/fitman/Downloads/anlzerVM/updates/training_english/models/model_english.pkl'
es_model = '/home/fitman/Downloads/anlzerVM/updates/training_spanish/models/model_spanish.pkl'