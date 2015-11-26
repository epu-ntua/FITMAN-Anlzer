User Related API Calls
----------------------

| VERB   | PATH                                                          | DESCRIPTION                                                |
|--------|:-------------------------------------------------------------:|:----------------------------------------------------------:|
| POST   | /[hostname]/api/user                                          | Create a new user Parameters:first_name,last_name,password,username (all String)|
| GET    | /[hostname]/api/user                                          | Get a list of all users.                                   |
| GET    | /[hostname]/api/user/{userID}                                 | Get information about user with the given id.              |
****
Group Related API Calls
----------------------

| VERB   | PATH                                                          | DESCRIPTION                                                |
|--------|:-------------------------------------------------------------:|:----------------------------------------------------------:|
| GET    | /[hostname]/api/groups                                        | Get a list of all created groups.                          |
| GET    | /[hostname]/api/groups/{groupID}                              | Get information about the group with the given id.         |
| GET    | /[hostname]/api/groups/{groupID}/user                         | Get a list of users that belong to the group with groupID. |
| GET    | /[hostname]/api/groups/{groupID}/user/{userID}                | Get information of whether the specified user belongs to the group. |
| POST   | /[hostname]/api/groups/{id}/user/{userID}                     | Add the specified user to the group.                       |
| DELETE | /[hostname]/api/groups/{id}/user/{userID}                     | Delete the specified user from the group.                  |
| GET    | /[hostname]/api/groups/{id}/user/{userID}/privileges          | Get the specified user’s privileges inside the group.       |
| PUT    | /[hostname]/api/groups/{id}/user/{userID}/privileges          | Change the specified user’s privileges inside the group, i.e. give him advanced privileges. |
****
Project Related API Calls
----------------------

| VERB   | PATH                                                          | DESCRIPTION |
|--------|:-------------------------------------------------------------:|:--------------------------------------------------------------------------------------------------------------:|
| GET    | /[hostname]/api/project                                       | Get a list of existing projects.                           |
| POST   | /[hostname]/api/project                                       | Create a new project. Parameters: Name(String), Created_by(UserID)| 
| GET    | /[hostname]/api/project/{projectID}                           | Get information about project with id projectID.           |
| DELETE | /[hostname]/api/project/{projectID}                           | Delete project. |
| PUT    | /[hostname]/api/project/{projectID}                           | Update project (Update all project fields in one request). |
| PATCH  | /[hostname]/api/project/{projectID}                           | Update project (Update one specific project field in one request). |
| PUT    | /[hostname]/api/project/{projectID}/train                     | Train the sentiment analysis system. Parameter: file (txt/csv) |
| GET    | /[hostname]/api/project/{projectID}/settings                  | Get the project settings.                                  |
| GET    | /[hostname]/api/project/{projectID}/group                     | Get the group to which the specified project belongs.      |
| GET    | /[hostname]/api/project/{projectID}/report                    | Get a list of reports of the specified project.            |
| POST   | /[hostname]/api/project/{projectID}/report                    | Create a report for the specified project. Parameters: datepicker_from(Date), datepicker_to(Date), facebook(String), keywords(String), lan(en/es), query_logic(AND/OR), query_name(String), twitter(String)| 
| GET    | /[hostname]/api/project/{projectID}/report/{reportID}         | Get information about the parameters of the specified report. |
| DELETE | /[hostname]/api/project/{projectID}/report/{reportID}         | Delete a report from a project.                            |
| GET    | /[hostname]/api/project/{projectID}/report/{reportID}/results | Get the results of the specified report.                   |