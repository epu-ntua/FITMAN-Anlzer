#twitter app
consumer_key = ""
consumer_secret = ""
access_token_key = ""
access_token_secret = ""

#facebook app
fb_access_token = ""

#couchbase configuration
cb_server = "localhost"
couchbase_port = 8091
cb_admin_username = "Administrator"
cb_admin_password = "anlzer"
cb_twitter_bucket = "anlzer"
cb_facebook_bucket = "anlzer"

#path for sentiment queue, i.e. to store temp files until they are given a sentiment tag - this directory will be created if it does not exist
sentimentQ = '/home/anlzer/Downloads/'

#svm model directories - these directories will be created during system training, if they don't exits already. If system training is not performed and dirs are not created, scripts WILL FAIL
en_model = '/home/anlzer/sentiment/training_english/models/' #english
es_model = '/home/anlzer/sentiment/training_spanish/models/' #spanish
