--------------------------------
Step by step installation guide
--------------------------------

Before starting, make sure you have Python 2.7 installed on your system or otherwise install.

1)	Download, install and start Couchbase Server.
You can find detailed information here:
http://www.couchbase.com/nosql-databases/couchbase-server
and
http://docs.couchbase.com/admin/admin/Install/Ubuntu-install.html
(instructions for different OS also available)


At this point you should have Couchbase Server running at your system.
You can now use your browser to access Couchbase admin console at
http://localhost:8091
After you are done with the initial configuration of your server you can proceed to the next step.

2)  Install the Java runtime required for Elasticseacrh installation. Elasticsearch recommends Java runtime, Oracle Java, but for Anlzer the openjdk-7-jre was successfully tested.

3)	Download and install (i.e. extract contents from archive) Elasticsearch
http://www.elasticsearch.org/

4)	Download and install Kibana
http://www.elasticsearch.org/overview/kibana/
We recommend installing Kibana as an Elasticsearch plugin which is done in 4 simple steps: 
- extract archive contents
- rename parent Kibana forlder to _site
- create a new folder named kibana and copy _site folder in it
- copy the kibana forlder inside Elasticsearch folder, specifically inside [ES main folder]/plugins/
Now when you start Elasticsearch, Kibana will run as a plugin

5)	Download and install Couchbase transport plugin for Elasticsearch
https://github.com/couchbaselabs/elasticsearch-transport-couchbase
Make sure you choose the correct version depending on your Couchbase and Elasticsearch versions.

6)  Open elasticsearch.yml file and add the following three lines in the end:
- couchbase.port : 9091
- couchbase.username: Administrator
- couchbase.password: [your Couchbase Admin password]

Close the file and start Elasticsearch

7)	Create a Couchbase bucket through Couchbase web interface.
Choose memory quota according to the machine's memory capacity and your project's configurations
In the field about access control, choose standard port and provide a password

8)	Create an Elasticsearch index
> curl -XPUT http://localhost:9200/index_name

You can find detailed guides for Elasticsearch in the [official site](http://www.elasticsearch.org/).


9)	Close the created Elasticsearch index
> curl -XPOST http://localhost:9200/index_name/_close

10)	Create the index mapping using the two commands inside the file [ElasticSearch_CouchBase_settings_and_mapping.txt](./SocialMediaEnabler/socialEnabler/settings/ElasticSearch_CouchBase_settings_and_mapping.txt)
Run the two commands on a terminal. The one about the _settings should be run before the one about _mapping.

Note that the url used in both commands starts with
http://localhost:9200/anlzer/
Here anlzer is the name of the elasticsearch index. So to run the commands you should replace 'anlzer' with the name of your index.

11)	Open the configured Elasticsearch index.
> curl -XPOST http://localhost:9200/index_name/_open

12)	Create a   Cross-datacenter Replication  (xdcr) between your Couchbase bucket and your Elasticsearch index. In order to do that you can follow the instructions on the plugin's site [here](https://github.com/couchbaselabs/elasticsearch-transport-couchbase)
You only need to follow the instructions regarding creating xdcr from Couchbase admin interface.

13)	Create a facebook application and get an application access token. You will need this for the facebook data retrieval script. Put this access token inside the [script settings file](SocialMediaEnabler/socialEnabler/scripts/script_settings.py) as a value in the field fb_access_token.

14)	Create a twitter application. You will need this for the twitter data retrieval script. Inside the [script settings file](SocialMediaEnabler/socialEnabler/scripts/script_settings.py) there are four fields related to twitter, under the "#twitter app" line. Use your twitter application data to fill in their values.

15) Review and update the rest of the settings in [script settings file](SocialMediaEnabler/socialEnabler/scripts/script_settings.py)
Couchbase password refers to the one from step 6, i.e. your bucket password, not the Administrator password

16)	Open [configuration file](UIapp/UIapp/configurations.py) and complete the urls appropriately according to your selected ports and names in the previous steps. (You can ignore the RSS related fields)
Couchbase password refers to the one from step 6, i.e. your bucket password, not the Administrator password

17) Install Couchbase Python SDK following the instructions [here](http://developer.couchbase.com/documentation/server/4.0/sdks/python-2.0/download-links.html)

18)	Install the requirements from [here](UIapp/requirements.txt)
> sudo pip install -r requirements.txt

19) Install scikit following the instructions [here](http://scikit-learn.org/stable/install.html)
Pay attention to the dependencies on numpy and scipy. Do not install scikit if these two requirements are not satisfied.


20)	Inside UIapp folder run the following command to initialize the Django application database
> python manage.py syncdb

21)	Again inside UIapp folder run 
> python manage.py runserver 0.0.0.0:8000 &


Anlzer is ready to be accessed from its web interface at http://localhost:8000
From the FreeSearch menu item you can choose to load and store the provided pre-configured Kibana dashboard, unless you prefer to experiment on your own...
You can also access Anlzer's api from http://localhost:8000/api
Enjoy!

For what to do next, look [here](UIapp/README.md) and [here](SocialMediaEnabler/socialEnabler/scripts/README.md)
