#general settings
server_ip = ''

#rapidanalytics settings
rapidanalytics_path = 'http://localhost:8081/RA/public_process/'

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
sentiment_training_path = rapidanalytics_path+'sentimentTrain'
kibana_path='http://'+server_ip+':9200/_plugin/kibana/index.html#/dashboard/elasticsearch/'
twitter_connector = rapidanalytics_path
facebook_connector = rapidanalytics_path

#svm model files
en_model = '/home/fitman/Downloads/anlzerVM/updates/training_english/models/model_english.pkl'
es_model = '/home/fitman/Downloads/anlzerVM/updates/training_spanish/models/model_spanish.pkl'