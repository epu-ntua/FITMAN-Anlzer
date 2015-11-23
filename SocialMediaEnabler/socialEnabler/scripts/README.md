------------------
Important note
------------------
This folder contains multiple important python scripts, used to handle data retrieval and storage, nlp and sentiment analysis. This file describes the functionality of those scripts that the system admin will need to interact with.

-------------------
script_settings.py
-------------------

This is the file to store all required information by the other scripts, like passwords, application tokens, usernames etc.
Before starting the data retrievers, a project should be created and configured either from the UI or through the api. The 1st Anlzer project is the master project to which all scripts are connected.

----------------
retrievers/facebook.py
----------------

This script is used to schedule retrieval of facebook posts and comments from specific public Facebook pages. The user of Anlzer can configure these pages through the application's web interface.

The system admin can schedule this python script to run as a cron job whenever he finds it suitable, according to the Facebook pages' expected traffic. 

In order for this script to work properly, you need to create a facebook application and fill in the required token in script_settings.py

----------
retrievers/twitter.py
----------

This script opens a twitter stream and retrieves all tweets that contain specific words or are made from specific accounts. The user of Anlzer can configure these settings through the application's web interface.

The system admin only needs to start this python script, after configuring the necessary information in script_settings.py. Please note that the creation of a Twitter application is necessary in order for the script to run.


------------------------------------------
sentiment-process/update_keys.py and sentiment-process/update_keys_spanish.py
------------------------------------------

The system admin simply needs to start these scripts in order for the sentiment analysis process to run. 
The file CBConnector.py is used by these scripts.


----------------
requirements.txt
----------------
You can install the required python libraries with the command
sudo pip install -r requirements.txt
*Attention* Refer to couchbase-server website for more information on using the Couchbase API for Python developers. There are some prerequisites you need to install before installing the Python lib. 
 You can also find more information in this repository's main README.md
If you followed the instructions in the main InstallationGuide, you do not need to re-install these requirements 



