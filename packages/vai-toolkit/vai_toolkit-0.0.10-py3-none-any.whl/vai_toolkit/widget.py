from vai_toolkit.client import *
import json



## email group add, get

def get_email_groups(user_secret, pipeline_key) -> list:
    """This method is used to get email list for given pipeline of user.

    args:

        user_secret {string}: It is the user secret key.
        pipeline_key {string}: It is the pipeline key.

    returns:

        type: List of all email groups object.
    
    Example:

        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import widget

        user_secret = 'USER_SECRET_KEY'
        pipeline_key = 'PIPELINE_KEY'

        res = widget.get_email_groups(user_secret, pipeline_key )
        </span>
        </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">[
            {
                "_id": "6204f736f758710015aeceac",
                "name": "EMAIL_GROUP_NAME",
                "users": [
                    "john.doe@gmail.com"
                ]
            }
        ]</span>
        </code></pre>
    """

    headers =create_headers(user_secret,pipeline= pipeline_key)

    payload = json.dumps({
            "functionName" : "get_email_groups",
        })

    return validate_response(payload, headers)


def create_email_groups(user_secret, pipeline_key, group_name, email_list) -> object:
    """This method is used to create email list use in widget for sending the survey.
    
    args:

        user_secret {string}: It is the user secret key.
        pipeline_key {string}: It is the pipeline key.
        group_name {string} : It is the name of group to give.
        email_list {array}: It is the users array consist of object which are having email, firstName, and lastName keys.

    returns: 

        type: Created email group response object.

    Example:

        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import widget

        user_secret = 'USER_SECRET_KEY'
        pipeline_key = 'PIPELINE_KEY'
        groupName = 'Group 1'
        email_list =  [ { email : "john.deo@gmail.com" ,firstName : "John" , lastName : "Deo"  }]

        res = widget.create_email_groups(user_secret, pipeline_key , groupName, email_list)
        </span>
        </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
            "groupName": "Group 1",
            "users": [
                {
                    "email": "john.deo@gmail.com",
                    "firstName": "John",
                    "lastName": "Deo",
                    "isSelected": true,
                    "_id": "64b78349f0a90246a2a2c6b5"
                }
            ],
            "creator": "61efccd707170700131a87c2",
            "isDeleted": false,
            "createdAt": "2023-07-19T06:31:37.465Z",
            "updatedAt": "2023-07-19T06:31:37.465Z",
            "_id": "64b78349f0a90246a2a2c6b4",
            "pipeline": "64b776fbf0a90246a2a2c3c0",
        }</span>
        </code></pre>
    """

    headers =create_headers(user_secret,pipeline= pipeline_key)

    payload = json.dumps({
            "functionName" : "create_email_groups",
            "groupName": group_name,
            "users": email_list ,
        })

    return validate_response(payload, headers)


def create_panel(user_secret, pipeline_key, name):
    headers =create_headers(user_secret,pipeline= pipeline_key)

    payload = json.dumps({
            "functionName" : "create_panel",
            "name": name,
        })

    return validate_response(payload, headers)


## data tracker widget

def create_widget(user_secret, pipeline_key, widget_title, controlPanel, columns) -> object:
    """This method is used to add data tracker widget of timeseries off for given pipeline of user.
    
    args:

        user_secret {string}: It is the user secret key.
        pipeline_key {string}: It is the pipeline key.
        widget_title {string} : It is the name of widget you want to give
        controlPanel {string}: It is the object id of control panel widget of which you want to get prediction.
        columns {array}: It is the list of numeric column fields to which include in widget.

    returns: 

        type: Created widget response object.

    Example:

        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import widget

        user_secret = 'USER_SECRET_KEY'
        pipeline_key = 'PIPELINE_KEY'
        widget_title = 'WIDGET_TITLE'
        controlPanel = 'PANEL ID'
        columns= ["race", "hours-per-week", "age"]

        res = widget.create_widget(user_secret, pipeline_key , widget_title, controlPanel, columns)
        </span>
        </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
            '_id': '64b7b4e4de9be445d40d7cc8', 
            'widgetName': 'WIDGET_TITLE',
            'creator': '5e996c09e667701bdc9c7546', 
            'pipeline': '64a2c873ff2ea7f10cb83f94',
            'dataSetFields': ['GuestCount']
        }</span>
        </code></pre> 
    """
    
    headers =create_headers(user_secret, pipeline= pipeline_key)

    payload = json.dumps({ 
            "functionName": "create_widget",
            "name": widget_title,
            "controlPanel": controlPanel,
            "dataSetFields": columns
        })

    return validate_response(payload, headers)


def create_timeseries_widget(user_secret, pipeline_key, panel_id, name, type) -> object:
    """This method is used to add data tracker widget of timeseries on for given pipeline of user.
    
    args:

        user_secret {string}: It is the user secret key.
        pipeline_key {string}: It is the pipeline key.
        panel_id {string} : It is the object id of panel which you want to get prediction.
        name {string}: It is the name of widget you want to give.
        type {string}: It is the type of timeseries. It could be only 'WEEK' or 'HOUR'

    returns: 

        type: Created timeseries widget response object.

    Example:

        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import widget

        user_secret = 'USER_SECRET_KEY'
        pipeline_key = 'PIPELINE_KEY'
        name= 'WIDGET_TITLE'
        panel_id = 'PANEL ID'
        type = 'HOUR'

        res = widget.create_timeseries_widget(user_secret, pipeline_key, panel_id, name, type)
        </span>
        </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
            "_id": "64b78462f0a90246a2a2c6eb",
            "creator": "61efccd707170700131a87c2",
            "pipeline": "64b776fbf0a90246a2a2c3c0",
            "name": "WIDGET_TITLE"
        }</span>
        </code></pre>
    """
    
    headers =create_headers(user_secret,pipeline= pipeline_key)
    
    payload =json.dumps({
        "functionName": "create_timeseries",
        "panel" :panel_id,
        "name":name,
        "type" :type
        })

    return validate_response(payload, headers)



## survey widgets
 
def list_survey(user_secret, pipeline_key) -> list:
    """This method is used to get list of survey panel for given pipeline of user. 
    
    args:

        user_secret {string}: It is the user secret key.
        pipeline_key {string}: It is the pipeline key.

    returns: 

        type: List of survey panel objects in provided pipeline and user.

    Example:

        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import widget

        user_secret = 'USER_SECRET_KEY'
        pipeline_key = 'PIPELINE_KEY'

        res = widget.list_survey(user_secret, pipeline_key )
        </span>
        </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">[
            {
                "_id": "64b7838ef0a90246a2a2c6c6",
                "pipeline": "64b776fbf0a90246a2a2c3c0",
                "name": "Test 1"
            }
        ]</span>
        </code></pre>
    """

    headers =create_headers(user_secret,pipeline= pipeline_key)
        
    payload = json.dumps({ 
        "functionName": "list_survey",
    })    

    return validate_response(payload, headers)


def create_survey_panel(user_secret, pipeline_key, panel_name) -> object:
    """This method is used to add survey panel for given pipeline of user.
    
    args:

        user_secret {string}: It is the user secret key.
        pipeline_key {string}: It is the pipeline key.
        panel_name {string}: It is control panel name

    returns: 

        type: Created survey panel response object.

    Example:

        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import widget

        user_secret = 'USER_SECRET_KEY'
        pipeline_key = 'PIPELINE_KEY'
        panel_name= 'PANEL_NAME'

        res = widget.create_survey_panel(user_secret, pipeline_key ,panel_name)
        </span>
        </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
            "_id": "64b7838ef0a90246a2a2c6c6",
            "creator": "61efccd707170700131a87c2",
            "pipeline": "64b776fbf0a90246a2a2c3c0",
            "panel_name": "PANEL_NAME"
        }</span>
        </code></pre>
    """
    
    headers =create_headers(user_secret, pipeline = pipeline_key)

    payload =json.dumps({
            "functionName": "create_survey_panel",
            "name": panel_name,
        })

    return validate_response(payload, headers)


def create_survey(user_secret, pipeline_key, panel_id, widget_title, questions) -> object:
    """This method is used to add survey question widget for given pipeline of user.
    
    args:

        user_secret {string}: It is the user secret key.
        pipeline_key {string}: It is the pipeline key.
        panel_id {string} : It is the object id of panel which you want to get prediction.
        widget_title {array}: It is the name of widget you want to give.
        questions {array}: It is array consist of question to and respective answers.

    returns: 

        type: Created survey object.

    Example:

        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import widget

        user_secret = 'USER_SECRET_KEY'
        pipeline_key = 'PIPELINE_KEY'
        widget_title= 'WIDGET_TITLE'
        panel_id = 'PANEL ID'
        questions= [
            {
                "queType": "SINGLE_ANSWER",
                "queName": "Name OF QUESTION",
                "options": [
                    {
                        "option": "Option A"
                    },
                    {
                        "option": "Option B"
                    }
                ]
            }
        ]

        res = widget.create_survey(user_secret, pipeline_key , widget_title, panel_id, questions)
        </span>
        </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
            "_id": "64b784eaf0a90246a2a2c705",
            "widgetName": "WIDGET_TITLE",
            "creator": "61efccd707170700131a87c2",
            "pipeline": "64b776fbf0a90246a2a2c3c0",
            "customAnalytics": "648171758ae9ce41584b8d02",
            "question": [
                {
                    "queName": "Name OF QUESTION",
                    "queType": "SINGLE_ANSWER",
                    "options": [
                        {
                            "option": "Option A",
                            "lowQueQuality": null,
                            "highQueQuality": null,
                            "_id": "64b784eaf0a90246a2a2c707"
                        },
                        {
                            "option": "Option B",
                            "lowQueQuality": null,
                            "highQueQuality": null,
                            "_id": "64b784eaf0a90246a2a2c708"
                        }
                    ],
                    "isOptionOther": false,
                    "optionDescription": null,
                    "_id": "64b784eaf0a90246a2a2c706"
                }
            ]
        }</span>
        </code></pre> 
    """
    
    headers =create_headers(user_secret,pipeline= pipeline_key)

    payload= json.dumps({
            "functionName": "create_survey",
            "panel" :panel_id,
            "widgetName": widget_title,
            "questions" :questions
        })

    return validate_response(payload, headers)


def update_survey(user_secret, pipeline_key, old_survey_name, new_survey_name) -> object:
    """This method is used to update survey name. 
    
    args:

        user_secret {string}: It is the user secret key.
        pipeline_key {string}: It is the pipeline key.
        old_survey_name {string} : It is the old name of survey which want to update.
        new_survey_name {array}: It is the new name of survey to update.
        
    returns: 

        type: Updated survey response object.

    Example:

        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import widget

        user_secret = 'USER_SECRET_KEY'
        pipeline_key = 'PIPELINE_KEY'
        old_survey_name= 'OLD_SURVEY_NAME'
        new_survey_name = 'NEW_SURVEY_NAME'

        res = widget.update_survey(user_secret, pipeline_key ,old_survey_name, new_survey_name)
        </span>
        </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
            "_id": "64b78422f0a90246a2a2c6df",
            "creator": "61efccd707170700131a87c2",
            "pipeline": "64b776fbf0a90246a2a2c3c0",
            "name": "NEW_SURVEY_NAME"
        }</span>
        </code></pre>
    """

    headers =create_headers(user_secret,pipeline= pipeline_key)

    payload =json.dumps({
        "functionName": "update_survey",
        "surveyName": old_survey_name,
        "newSurveyName": new_survey_name,
    })

    return validate_response(payload, headers)
