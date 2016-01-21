------------
Introduction
------------

The FITMAN “Unstructured and Social Data Analytics” Specific Enabler (FITMAN-Anlzer) aims at extracting unstructured data from selected social media platforms and web resources and at turning such user-generated content to knowledge to be used for the benefit of any manufacturing stakeholder. 
It is responsible for:

>1. Acquiring information based on predefined keywords and / or accounts / pages,
2. Filtering relevant information (i.e. removing keywords and URLs),
3. Running opinion mining and trend analysis techniques (based on the SVM algorithm) and
4. Presenting the emerging topics, sentiments and trends in an interactive way through intuitive visualizations 
(i.e. dashboards, tree maps, charts, galleries)..

In order to provide credible outcomes, it is crucial:
* to guide the Specific Enabler where it is going to search for specific patterns and interrelate data and
* to train the Specific Enabler with the relative vocabulary and data of each industry and in the necessary language(s).
In both cases, the user is prompted to provide the necessary settings and information during the initialization procedure before he is able to execute any query to the collected unstructured data. 

The period during which data are collected may span from the past to the future according to the restrictions imposed by the social media platforms APIs and the user preferences. In general, the whole procedure of collecting data is repeated periodically, which eventually affects the system scalability capabilities; the more frequent the crawling process on data and the processing of them is, the less scalable the U-SDA SE becomes. By default, Twitter data are updated almost real time, whereas Facebook retrieval runs once a day. 

Upon analyzing the gathered information for every query, Anlzer SE visualizes the topics identified from specific social media platforms and web resources, gives a trending line and also the *sentiment indicator* for every topic identified. The users may also save the queries they have executed, in order to view the updated results whenever needed. 

-----------------
SPECIAL THANKS
-----------------

[Couchbase-server] (http://www.couchbase.com/nosql-databases/couchbase-server)

[Elasticsearch] (https://www.elastic.co/products/elasticsearch)

[Kibana] (https://www.elastic.co/products/kibana)

[Django] (https://www.djangoproject.com/)


-----------------
Build and Install
-----------------

You can find [here](./InstallationGuide.md) a detailed guide for the installation and configuration of Anlzer SE. 
 
The following are prerequisites you need to install in order to successfully use all the functionalities: 

Java (JRE 7)
Couchbase Server (Community Edition 3.0.1)
Elasticsearch (1.7.3)
Kibana (v3.1.3)
Couchbase transport plugin for Elasticsearch
Python (2.7)
Django (1.8)

The versions listed here are the ones used for the anlzer vm which you can download through [FITMAN catalogue](http://catalogue.fitman.atosresearch.eu/enablers/unstructured-and-social-data-analytics) 
All of the above are available both for Linux and Windows. That said, Anlzer has been developed and tested under Ubuntu (12.04) and this is the proposed OS for the installation.
Should you choose to use newer versions of the required software (which is strongly advisable as new versions include bug fixes and security updates), make sure to check for possible incompatibilities. As an example, make sure there is a Couchbase transport plugin for the selected Couchbase Server and Elasticsearch versions.


-------------
Usage Example
-------------

Anlzer is a web platform. For detailed usage examples and application screenshots, please visit
http://catalogue.fitman.atosresearch.eu/enablers/documentation
