--------------------------------
Step by step installation guide
--------------------------------


Before starting, make sure you have Python 2.7, JRE 1.6, JRE 1.7 and MySQL server installed in your system or otherwise install them.

1)	Download, install and start Couchbase Server.
You can find detailed information here:
http://www.couchbase.com/nosql-databases/couchbase-server
and
http://docs.couchbase.com/admin/admin/Install/Ubuntu-install.html
(instructions for different OS also available)

2)	Download, install and start Elasticsearch
http://www.elasticsearch.org/

3)	Download and install Kibana
http://www.elasticsearch.org/overview/kibana/

4)	Download and install Couchbase transport plugin for Elasticsearch
https://github.com/couchbaselabs/elasticsearch-transport-couchbase

At this point you should have Couchbase Server running at your system.
You can now use your browser to access Couchbase admin console at
http://localhost:8091
After you are done with the initial configuration of your server you can proceed to the next step.

5)	Create a Couchbase bucket through Couchbase web interface.
Choose memory quota according to the machine’s memory capacity and your project’s configurations

6)	Create an Elasticsearch index
> curl -XPUT http://localhost:9200/index_name

You can find detailed guides for Elasticsearch in the [official site](http://www.elasticsearch.org/).


7)	Close the created Elasticsearch index
> curl -XPOST http://localhost:9200/index_name/_close

8)	Create the index mapping using the two commands inside the file [ElasticSearch_CouchBase_settings_and_mapping.txt](./SocialMediaEnabler/socialEnabler/settings/ElasticSearch_CouchBase_settings_and_mapping.txt)
Run the two commands on a terminal. The one about the _settings should be run before the one about _mapping.

Note that the url used in both commands starts with
http://localhost:9200/twitter/
Here twitter is the name of the elasticsearch index. So to run the commands you should replace “twitter” with the name of your index.

9)	Open the configured Elasticsearch index.
> curl -XPOST http://localhost:9200/index_name/_open

10)	Create a   Cross-datacenter Replication  (xdcr) between your Couchbase bucket and your Elasticsearch index. In order to do that you can follow the instructions on the plugin’s site [here](https://github.com/couchbaselabs/elasticsearch-transport-couchbase)

11)	 Install [Rapidminer](https://rapidminer.com/products/studio/)
In order  to install Rapidminer 5.3 you must use Java 7. To choose between Java 6 and 7, run the following command on terminal and choose appropriately.
> sudo update-alternatives --config java

12)	 Install text mining extension for Rapidminer.

13)	 Install [Rapidanalytics](https://rapidminer.com/products/server/)
For the above version of Rapidanalytics you must use Java 6.
You will need to create and configure a MySQL database and user. Please refer to the Rapidanalytics manual for a detailed installation guide.
The server should listen to a port different from 8000 and 8080. The default used in our configuration is 8081. Should you choose a different one, you will later need to make the necessary changes to the anlzer’s Django application settings.

14) Install text mining extension for Rapidanalytics (It is actually the same with the one for Rapidminer)

15)	Start Rapidanalytics server

16)	Open Rapidminer Studio and create a remote repository connected to the Rapidanalytics Server

17)	From Rapidanalytics Web Interface create an anonymous user (the assigned password is not important)

18)	 Again inside Rapidanalytics Web Interface, go to system settings and create the following two variables:
com.rapidanalytics.web.anonymous_resources  with value true
com.rapidanalytics.web.anonymous_services with value true
If they were created successfully you should be able to see them now inside system information/system settings

19)	Give read, write and run permissions to the anonymous user on the remote repository’s folder inside Rapidanalytics repository

20)	Create and configure the required MySQL database, by running the following command from terminal from insiide the path of [this file](./SocialMediaEnabler/socialEnabler/scripts/sql_commands.txt)
> mysql -h localhost -u root -p < sql_commands.txt

You will be prompted for your MySQL root password.

21)	Import all rapidminer processes from [here](./SocialMediaEnabler/socialEnabler/rapidminer/anonymous_rapidanalytics) to the remote repository insideRapidminer

22)	Make sure to update the paths inside the processes in order to define valid paths inside the local file system for the creation and manipulation of files and check connectivity to the MySQL database.

You should also update the path to the Spanish stopwords file inside the following two processes: SpanishSentiTrainWithNgrams and SpanishUseLearntModel
The file containing the stopwords is "spanish stopwords.txt" and it is located [here](SocialMediaEnabler/socialEnabler/settings/)
Be sure to update the path depending on its location inside your local file system.

23)	From the Rapidanalytics web interface select the following processes and expose them as services:
•	storeFBaccounts
•	storeKeywords
•	storeTWaccounts
•	SentiTrainWithNgrams
•	readUpdates
•	SpanishSentiTrainWithNgrams
•	SpanishreadUpdates

Create a cron trigger for the following two processes (proposed time every 15’)
•	UseLearntModel
•	SpanishUseLearntModel


24)	Create a facebook application and get an application access token. You will need this for the facebook data retrieval script. Put this access token inside the [script settings file](SocialMediaEnabler/socialEnabler/scripts/script_settings.py) as a value in the field fb_access_token.

25)	Create a twitter application. You will need this for the twitter data retrieval script. Inside the [script settings file](SocialMediaEnabler/socialEnabler/scripts/script_settings.py) there are four fields related to twitter, under the "#twitter app" line. Use your twitter application data to fill in their values.

26)	Open file UIapp/UIapp/configurations.py and complete the urls appropriately according to your selected ports and names in the previous steps. (You can ignore the RSS related fields)

27)	Install the requirements in UIapp/requirements.txt
> sudo pip install -r requirements.txt

28)	Inside UIapp folder run the following command to initialize the Django application database
> python manage.py syncdb

29)	Again inside UIapp folder run 
> python manage.py runserver 0.0.0.0:8000 &

30)	Anlzer is ready to be accessed from its web interface at http://localhost:8000
