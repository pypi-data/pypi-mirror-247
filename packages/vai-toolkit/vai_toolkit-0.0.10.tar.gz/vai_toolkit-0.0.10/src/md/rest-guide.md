# REST API

This is our Python Guide for ML development. See Tables. Below

<br>
Table 1. client()

| Method                                                                 | Description                                                       |
| ---------------------------------------------------------------------- | ----------------------------------------------------------------- |
| [client.create_organization()](#create_organization)| This method is used to create organization for user.              |
| [client.update_name()](#update_name)                | This method is used to update user's first name and last name.    |
| [client.update_password()](#update_password)        | This method is used to update user password.                      |

<!-- 
| Method                                                                 | Description                                                       |
| ---------------------------------------------------------------------- | ----------------------------------------------------------------- |
| [client.create_account()](#create_account)          | This method is used to create new user account.                   |
| [client.create_connection()](#create_connection)    | This method is used to create connection and get token.           |
| [client.create_organization()](#create_organization)| This method is used to create organization for user.              |
| [client.login()](#login)                            | This method is used to verify user.                               |
| [client.update_name()](#update_name)                | This method is used to update user's first name and last name.    |
| [client.update_password()](#update_password)        | This method is used to update user password.                      | -->

<br>

<br>
Table 2. pipeline()

| Method                                                           | Description                                                                          |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [pipeline.create_pipeline()](#vai_toolkit.pipeline.create)                | This method is used to create pipeline of provided user.                             |
| [pipeline.create_alert()](#vai_toolkit.pipeline.create_alert)    | This method is used to create alert for given pipeline of user.                      |
| [pipeline.create_table()](#vai_toolkit.pipeline.create_table)                | This method is used to create table for given pipeline of user.                             |
| [pipeline.delete_table()](#vai_toolkit.pipeline.delete_table)                | This method is used to delete table for given pipeline of user.                          |
| [pipeline.get_table()](#vai_toolkit.pipeline.get_table)      | This method is used to get tables of given pipeline of user.            |
| [pipeline.list_alerts()](#vai_toolkit.pipeline.list_alerts)      | This method is used to get the list of alerts for given pipeline of user.            |
| [pipeline.set_default_table()](#vai_toolkit.pipeline.set_default_table)    | This method is used to set default table for given pipeline of user.                    |
| [pipeline.update_table()](#vai_toolkit.pipeline.update_table)    | This method is used to update table name for given pipeline of user.                         |

<br>

<br>
Table 3. data()

| Method                                                    | Description                                                           |
| --------------------------------------------------------- | --------------------------------------------------------------------- |
| [data.delete_data()](#delete_data)      | This method is used to delete dataset data for given range in pipeline of user.      |
| [data.download_csvs()](#download_csvs)   | This method is used to download dataset for given pipeline of user.   |
| [data.list_labels()](#list_labels)       | This method is used to get labels for given pipeline of user.         |
| [data.set_labels()](#set_labels)         | This method is used to set labels for given pipeline of user.         |
| [data.set_relations()](#set_relations)         | This method is used to set relations between tables of given pipeline of user.                 |
| [data.upload_data()](#upload_data)       | This method is used to upload data for given pipeline of user.        |

<br>

<br>
Table 4. model()

| Method                                                               | Description                                                                                                                                 |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| [model.explain()](#explain)            | This method is used to get explanability values of specific record for given pipeline of user with the model trained having timeseries off. |
| [model.explain_timeseries()](#explain_timeseries)  | This method is used to get explanability values of specific record for given pipeline of user with the model trained having timeseries on.  |
| [model.explain_link()](#explain_link)  | This method is used to get explanability values of of next link.  |
| [model.predict_time()](#predict_time)              | This method is used to get prediction of table count.                                                                                       |
| [model.predict_next_link()](#predict_next_link)              | This method is used to get prediction of next link model.                                                                                       |
| [model.train_mixed()](#train_mixed)                | This method is used to train model with timeseries off for given pipeline of user.                                                          |
| [model.train_timeseries()](#train_timeseries)      | This method is used to train model with timeseries on for given pipeline of user.                                                           |
| [model.next_link()](#next_link)      | This method is used to create model next link type.                                                           |
| [model.delete_model()](#delete_model)      | This method is used to delete given model. |
| [model.retrain_model()](#retrain_model)      | This method is used to retrain given model. |

<br>

Our RESTAPI is one API call with one-to-one lineup with the Python API. The methods are values for the key "func" and the

<!-- Table 1.  

Field | Value   
:-------: | :------:
HTTP Method   |POST
Request Format | json-payload
Response Format| json
Request URL    | [https://dev-cloud-api.virtuousai.com/vai-toolkit](https://dev-cloud-api.virtuousai.com/vai-toolkit) -->

Method
<pre class="content-block"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">curl -X post https://dev-cloud-api.virtuousai.com/vai-toolkit</span>
</code></pre>

Payload:
<pre class="content-block"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">https://dev-cloud-api.virtuousai.com/vai-toolkit</span>
</code></pre>

<br><br><br>

## client

<br>

### create_organization

<u>Method Details :</u>

>>This metod is used to create organization for user.
>
>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.

>>
<u>Payload :</u>
>>>
    "functionName": "create_organization"
>>>>
It is the function name to identify request.
>>>
    "name": "ORGANIZATION_NAME"
>>>>
It is the name of organization.
>>>
    "users":  {  "EMAIL_TO_ASSIGN" :"ROLE_OF_THAT_USER" }
>>>>
Password to provide which is to be use while login in platform.

>>
Example's argument:
>>>

<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "create_organization",
    "name": "ORGANIZATION_NAME",
    "users":{  "EMAIL_TO_ASSIGN" :"ROLE_OF_THAT_USER" }
}</span>
</code></pre>

>>
Output:
>>
    {
        "user": "61efccd707170700131a87c2",
        "name": "ORGANIZATION_NAME",
        "datasetS3TotalSize": 0,
        "isDeleted": false,
        "createdAt": "2023-07-19T05:34:13.391Z",
        "updatedAt": "2023-07-19T05:34:13.391Z",
        "_id": "64b775d5f0a90246a2a2c31a"
    }

### update_name

<u>Method Details :</u>

This method is used to update user's first name and last name.
>
>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.

>>
<u>Payload :</u>
>>>
    "functionName": "update_name"
>>>>
It is the function name to identify request.

>>>
    "firstName": String
>>>>
First name of the user to update.
>>>
    "lastName":  String
>>>>
Last name of the user to update.
>>
Example's argument:
>>>

<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "update_name",
    "firstName": "John",
    "lastName": "Deo"
}</span>
</code></pre>
>>
Output:
>>
    {
        "email": "john.deo@gmail.com",
        "_id": "61efccd707170700131a87c2",
        "firstName": "John",
        "lastName": "Deo",
    }
<br>
<br>

### update_password

<u>Method Details :</u>

>
This method is used to update user password.
>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.

>>
<u>Payload :</u>
>>>
    "functionName": "update_password"
>>>>
It is the function name to identify request.
>>>
    "password":  "PASSWORD"
>>>>
New password to the account.

>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "update_password",
    "password": "NEW_SECURE_PASSWORD"
}</span>
</code></pre>

>>
Output:
>>
    {
        "message": "Password changed successfully!.."
    }
<br>
<br>

<br>
<br><br><br>

## pipeline

<br>

### create_pipeline

<u>Method Details :</u>

>
This method is used to create pipeline of provided user.
>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.

>>
<u>Payload :</u>
>>>
    "functionName": "create_pipeline"
>>>>
It is the function name to identify request.
>>>
    "title":  "PIPELINE_NAME"
>>>>
Name of pipeline to assign.
>>>
    "type":  "TABULAR" or "GRAPH"
>>>>
Type of the pipeline

>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "create_pipeline",
    "title": "PIPELINE_NAME",
    "type": "PIPELINE_TYPE"
}</span>
</code></pre>
>>
Output:
>>
    {
        "_id": "64b776fbf0a90246a2a2c3c0",
        "title": "PIPELINE_NAME",
        "apiKey": "62388816-b26e-4eff-bae7-1b361dccb194-1689745147818"
    }

<br>
<br>

### create_alert

<u>Method Details :</u>

>
This method is used to create alert of provided user and pipeline.
>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.
>>
<u>Payload :</u>
>>>
    "functionName": "create_alert"
>>>>
It is the function name to identify request.
>>>
    "name" : String
>>>>
It is the name of alert to give.
>>>
    "type" :"DATASET"
>>>>
Type of alert.
>>>
    "from" : Date
>>>>
It is the from date, from which date alert is consider.
>>>
    "to" : Date
>>>>
It is the to date, to which date alert is consider.
>>>
    "columnFields" :Array
>>>>
It is the list of numeric column fields to which include in alert.
>>>
    "week" : 2
>>>>
It is the number of weeks, weeks of previous data to consider.
>>>
    "thresholdLimit" : 49
>>>>
It is limit value, if uploaded data cross the limit of provided thresholdLimit then send mail.

>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "create_alert",
    "data" : {
        "name":"ALERT_NAME",
        "type":"DATASET",
        "from": "1/1/2023",
        "to": "12/31/2023",
        "columnFields": ["race", "hours-per-week", "age"],
        "week": 2,  
        "thresholdLimit": 49
    }
}</span>
</code></pre>
>>
Output:
>>
    {
        "name": "ALERT_NAME",
        "type": "DATASET",
        "pipelineId": null,
        "modelId": null,
        "from": "1/1/2023",
        "to": "12/31/2023",
        "columnFields": [
            "race",
            "hours-per-week",
            "age"
        ],
        "week": 2,
        "thresholdLimit": 49,
        "timeWindow": {
            "window": null,
            "startTime": null,
            "endTime": null,
            "column": null,
            "dates": [],
            "times": [],
            "isHoliday": null,
            "holidays": [],
            "step": null
        },
        "createdAt": "2023-07-19T05:59:30.634Z",
        "updatedAt": "2023-07-19T05:59:30.634Z",
        "_id": "64b77bc26f7131868c0776a4"
    }

<br>
<br>

### create_table

<u>Method Details :</u>
>
This method is used to create table for given pipeline of user.

>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.

>>
<u>Payload :</u>
>>>
    "functionName": "create_table"
>>>>
It is the function name to identify request.
>>>
    "name" :String
>>>>
It is the name of table to give.

>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "create_table",
    "name": "TABLE NAME"
}</span>
</code></pre>

>>
Output:
>>
        {
            'success': True,
            'table': {'name': 'Table Name','pipeline': 'Pipeline id', '_id': 'Table Id'}
        }
  <br>
<br>

### delete_table

<u>Method Details :</u>
>
This method is used to delete table for given pipeline of user.

>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.
>>
<u>Payload :</u>
>>>
    "functionName": "delete_table"
>>>>
It is the function name to identify request.
>>>
    "name" :String
>>>>
It is the name of table to delete.

>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "delete_table",
    "name": "TABLE NAME"
}</span>
</code></pre>

>>
Output:
>>
        {
            "success":true, 
            "message": "Table deleted successfully."
        }
<br>
<br>

### get_table

<u>Method Details :</u>
>
This method is used to get tables of given pipeline of user.

>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.
>>
<u>Payload :</u>
>>>
    "functionName": "get_table"
>>>>
It is the function name to identify request.

>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "get_table"
}</span>
</code></pre>

>>
Output:
>>
        [
            {
                name : 'TABLE NAME',
                _id : 'Table id',
                pipeline : 'Pipeline id'
            },
            {
                name : 'TABLE NAME 2',
                _id : 'Table id',
                pipeline : 'Pipeline id'
            },
        ]
<br>
<br>

### list_alerts

<u>Method Details :</u>

>
This method is used to get list of alerts provided user and pipeline.
>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.
>>
<u>Payload :</u>
>>>
    "functionName": "list_alerts"
>>>>
It is the function name to identify request.

>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "list_alerts"
}</span>
</code></pre>
>>
Output
>>
    [
        {
            "name": "ALERT_NAME",
            "type": "DATASET",
            "pipelineId": null,
            "modelId": null,
            "from": "1/1/2023",
            "to": "12/31/2023",
            "columnFields": [
                "race",
                "hours-per-week",
                "age"
            ],
            "week": 2,
            "thresholdLimit": 49,
            "timeWindow": {
                "window": null,
                "startTime": null,
                "endTime": null,
                "column": null,
                "dates": [],
                "times": [],
                "isHoliday": null,
                "holidays": [],
                "step": null
            },
            "createdAt": "2023-07-19T05:59:30.634Z",
            "updatedAt": "2023-07-19T05:59:30.634Z",
            "_id": "64b77bc26f7131868c0776a4"
         }
    ]

<br>
<br>

### set_default_table

<u>Method Details :</u>
>
This method is used to set default table for given pipeline of user.

>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.

>>
<u>Payload :</u>
>>>
    "functionName": "set_default_table"
>>>>
It is the function name to identify request.
>>>
    "name" :String
>>>>
It is the name of table to set as default.

>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "update_password",
    "name": "TABLE NAME"
}</span>
</code></pre>

>>
Output:
>>
        {
            "success":true, 
            "message": "Default table successfully."
        }
<br>
<br>

### update_table

<u>Method Details :</u>
>
This method is used to update table name for given pipeline of user.

>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.

>>
<u>Payload :</u>
>>>
    "functionName": "update_table"
>>>>
It is the function name to identify request.
>>>
    "oldName": :String
>>>>
It is the name of current name of table.
>>>
    "newName":String
>>>>
It is the new name of table to update.
>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "update_password",
    "oldName": "TABLE NAME",
    "newName": "NEW NAME"
}</span>
</code></pre>

>>
Output:
>>
    {
        "success":true, 
        "message": "Name updated successfully."
    }
<br>
<br>

<br><br><br>

## data

<br>

### delete_data

<u>Method Details :</u>

>
This method is used to delete dataset data for given range in pipeline of user.
>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.
>>
<u>Payload :</u>
>>>
    "functionName": "delete_data"
>>>>
It is the function name to identify request.
>>>
    "from_date" : "09/05/2023"
>>>>
It is from date value in 'MM-DD-YYYY' format.
>>>
    "to_date" : "09/05/2023"
>>>>
It is to date value in 'MM-DD-YYYY' format.
>>>
    "table" : "TABLE_NAME"
>>>>
It is name of table to delete data.
>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
 "functionName": "delete_data",
 "from_date" : "09/05/2023",
 "to_date" : "09/05/2023",
 "table" : "TABLE_NAME"
}</span>
</code></pre>
>>
Output:
>>
    {
    "message": "Deleted successfully!.."
    }   

<br>
<br>
<br>

### download_csvs

<u>Method Details :</u>

>
This method is used to download dataset of provided user and pipeline.
>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.
>>
<u>Payload :</u>
>>>
    "functionName": "download_csvs"
>>>>
It is the function name to identify request.
>>>
    fromDate:  "DATE" 
>>>>
Date from which download consider.
>>>
    toDate: "DATE" 
>>>>
Date to  which download consider.
>>>
    "table" : "TABLE_NAME"
>>>>
It is name of table of you want to download data by defualt active table is selected.
>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "download_csvs",
    "fromDate": "07-07-2023",
    "toDate": "07-15-2023",
    "table": "TABLE NAME"
}</span>
</code></pre>
<br>
<br>

### list_labels

<u>Method Details :</u>

>
This method is used to get labels of provided pipeline and user.
>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.
>>
<u>Payload :</u>
>>>
    "functionName": "list_labels"
>>>>
It is the function name to identify request.
>>>
    "table" : "TABLE_NAME"
>>>>
It is name of table of you want to see labels by defualt active table is selected.

>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "list_labels",
    "table":"TABLE NAME"
}</span>
</code></pre>
>>
Output:
>>
    {
      "success": true,
      "details": {
        "Table Name": "Table NAME",
        "Column Names": LIST OF COLUMN NAMES,
        "Column Types": LIST OF COLUMN TYPES,
        "Column Labels": LIST OF COLUMN LABELS
      }
    }

<br>
<br>

### set_labels

<u>Method Details :</u>

>
This method is used to set labels of provided user and pipeline.
>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.
>>
<u>Payload :</u>
>>>
    "functionName": "set_labels"
>>>>
It is the function name to identify request.
>>>
    "columnLabels" : { "ID" : "Input", "EDUCATION": "Protected", "LOAN-APPROVED": "Output"  }
>>>>
It is dictionary containing the keys as the column of provided pipeline and values are Input, Protected and Output of that column as column label.
>>>
    "columnTypes" : { "ID" : "NUMBER", "EDUCATION": "STRING", "LOAN-APPROVED": "CATEGORICAL" }
>>>>
It is dictionary containing the keys as the column of provided pipeline and values are NUMBER, STRING, CATEGORICAL and TIME of that column as column type.
>>>
    "table" : "TABLE_NAME"
>>>>
It is name of table of you want to set labels by defualt active table is selected.

>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "set_labels",
    "columnLabels" : { "ID" : "Input", "EDUCATION": "Protected", "LOAN-APPROVED": "Output"  },
    "columnTypes" : { "ID" : "NUMBER", "EDUCATION": "STRING", "CAPITAL-GAIN": "CATEGORICAL" },
    "table":"TABLE NAME"
}</span>
</code></pre>
>>
Output:
>>
    {
        'tableName': 'TABLE NAME',
        'columnLabels': [None, 'Output', None, None, 'Input', None, None, None, None],
        'columnNames': ['A1', 'DimItemkey', 'RestaurantCustomerName', 'PLU', 'ItemDescription', 'ItemSubcategory', 'ItemCategory', 'ItemReportingCategory', 'ItemFNBCategory'],
        'columnTypes': ['CATEGORY', 'CATEGORY', 'CATEGORY', 'CATEGORY', 'STRING', 'CATEGORY', 'CATEGORY', 'CATEGORY', 'CATEGORY']
        'pipeline': 'pipeline id',
        '_id': 'Table id'
    }

<br>
<br>
<br>

### set_relations

<u>Method Details :</u>

>
This method is used to set relations between tables of given pipeline of user.
>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.
>>
<u>Payload :</u>
>>>
    "functionName": "set_relations"
>>>>
It is the function name to identify request.
>>>
    "primaryKeys" :{ "dim_item": "PLU", "check": "CheckKey", "check_item": "CheckItemKey" }
>>>>
It is an object where key represents the name of table, and it's value is considered as primary key column.
>>>
    "toTable" : "TABLE_NAME"
>>>>
It is the table name of which you want to set main table to bind other tables.
>>>
    "relations" : [{"from": "dim_item","toColumn": "ItemNumber"} ]
>>>>
It is an array consists of relation object, where object is { "from":"From table name",  "toColumn": "Where column of to table want to bind"}.

>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
      "functionName": "set_relations",
      "primaryKeys": {
        "dim_item": "PLU",
        "check": "CheckKey",
        "check_item": "CheckItemKey"
      },
      "toTable": "check_item",
      "relations": [
        {
          "from": "dim_item",
          "toColumn": "ItemNumber"
        },
        {
          "from": "check",
          "toColumn": "CheckKey"
        }
      ]
}</span>
</code></pre>
>>
Output:
>>
    {
      "success": true,
      "messsage": "Updated successfully."
    }

<br>
<br>
<br>

### upload_data

<u>Method Details :</u>

>
This method is used to add data of provided user and pipeline.
>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.
>>
<u>Payload :</u>
>>>
    "functionName": "upload_data"
>>>>
It is the function name to identify request.
>>>
    "data": { "id" : [0, 1, 2, 3], "Capital Gain" : [10000, 20000, 30000, 40000]}
>>>>
It is object containing keys as column names name values as list of values
>>>
    "date": ["09-10-2023", "09-10-2023", "09-10-2023", "09-10-2023" ]
>>>>
It is the list containing the list of date of the data
>>>
    "time": ["11:08:50", "11:08:50", "11:08:50", "11:08:50" ]
>>>>
It is the list containing the list of times of the data
>>>
    allowNewColumns
>>>>
It is the boolean value. If you want to allow new columns pass as true otherwise false
>>>
    allowDuplicate 
>>>>
It is the boolean value. If you want to allow duplicate values then pass true otherwise false
>>>
    allowNewCategory 
>>>>
It is the boolean value. If you want to allow new category  pass as true otherwise false
>>>
    "table" : "TABLE_NAME"
>>>>
It is name of table of you want to upload data.

>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "upload_data",
    "data": { "id" : [0, 1, 2, 3], "Capital Gain" : [10000, 20000, 30000, 40000]},
    "date":["09-10-2023", "09-10-2023", "09-10-2023", "09-10-2023" ],
    "time" : ["11:08:50", "11:08:50", "11:08:50", "11:08:50" ],
    "allowNewColumns" : true,
    "allowDuplicate" : true,
    "allowNewCategory" : true,
    "table" : "TABLE NAME"
}</span>
</code></pre>

>>
Output:
>>
    {
        "success": true,
        "data": "{\"dates\":[\"09-10-2023\"]}",
        "warning": "We insert the duplicate data if we found."
    }

<br>
<br>

## model

<br>

### explain

<u>Method Details :</u>

>
This method is used to get explanability values of specific record for provided user pipeline with the model trained having timeseries off.
>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.
>>
<u>Payload :</u>
>>>
    "functionName": "explain"
>>>>
It is the function name to identify request.
>>>
    datasetData: Object
>>>>
It is object containing keys as column names and values as it respective value of the row.
>>>
    modelId: ObjectId
>>>>
It is the  model key which you want to get prediction.
>>>
    dataset: Date
>>>>
It is the dataset date which you want to get prediction.

>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "explain",
    "datasetData" :  { "Capital Gain" : 100, "Loan Approved" : "true"},
    "modelId" : "ID of MODEL",
    "dataset" : "07-15-2023"
}</span>
</code></pre>

>>
Output:
>>
    {
        "success": true,
        "output": {
            "loan-approved": {
                "inputs": {
                    "age": [
                        0.056
                    ],
                    "capital-loss": [
                        0
                    ],
                    "education": [
                        -0.037
                    ],
                    "education-num": [
                        -0.008
                    ],
                    "hours-per-week": [
                        0.113
                    ],
                    "native-country": [
                        -0.006
                    ],
                    "occupation": [
                        -0.019
                    ],
                    "relationship": [
                        0.05
                    ],
                    "workclass": [
                        -0.011
                    ]
                },
                "outputs": [
                    0.138
                ]
            }
        },
        "payload": {
            "model": "dev/models/5e99761f522f057aeb4ed3c4/64412fa37a5a840c036a3fce/64a526df900b514e57881ef5_0.1_100_1000_1_17",
            "x": {
                "age": {
                    "type": "NUMBER",
                    "values": [
                        48
                    ]
                },
                "capital-loss": {
                    "type": "CATEGORY",
                    "values": [
                        0
                    ]
                },
                "hours-per-week": {
                    "type": "NUMBER",
                    "values": [
                        60
                    ]
                },
                "workclass": {
                    "type": "CATEGORY",
                    "values": [
                        "Self-emp-not-inc"
                    ]
                },
                "education": {
                    "type": "CATEGORY",
                    "values": [
                        "HS-grad"
                    ]
                },
                "education-num": {
                    "type": "CATEGORY",
                    "values": [
                        9
                    ]
                },
                "occupation": {
                    "type": "CATEGORY",
                    "values": [
                        "Craft-repair"
                    ]
                },
                "relationship": {
                    "type": "CATEGORY",
                    "values": [
                        "Husband"
                    ]
                },
                "native-country": {
                    "type": "CATEGORY",
                    "values": [
                        "England"
                    ]
                }
            },
            "y": {
                "loan-approved": {
                    "type": "CATEGORY"
                }
            },
            "file_paths": [
                "dev/dataset-files/5e99761f522f057aeb4ed3c4/64412fa37a5a840c036a3fce/64412fd67a5a840c036a40fd/04-14-2023.csv"
            ]
        },
        "response": {
            "StatusCode": 200,
            "ExecutedVersion": "$LATEST",
            "Payload": "{\"errorMessage\": \"\", \"traceback\": \"\", \"data\": {\"loan-approved\": {\"inputs\": {\"age\": [0.056], \"capital-loss\": [0.0], \"education\": [-0.037], \"education-num\": [-0.008], \"hours-per-week\": [0.113], \"native-country\": [-0.006], \"occupation\": [-0.019], \"relationship\": [0.05], \"workclass\": [-0.011]}, \"outputs\": [0.138]}}}"
        }
    }
<br>
<br>

### explain_timeseries

<u>Method Details :</u>

>
This method is used to get explanability values of specific record for provided user pipeline with the model trained having timeseries on.
>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.
>>
<u>Payload :</u>
>>>
    "functionName": "explain_timeseries"
>>>>
It is the function name to identify request.
>>>
    "panel": ObjectId
>>>>
It is the object id of custom panel widget of which you want to get prediction.
>>>
    "model": ObjectId
>>>>
It is the  model key which you want to get prediction.
>>>
    "fromDate" :Date
>>>>
It is the date of dataset in pipeline from which model will create.
>>>
    "toDate" : Date
>>>>
It is the date of dataset in pipeline to which model will create.

>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "explain_timeseries",
    "panel" : "PANEL_ID",
    "model" : "MODEL_ID",
    "fromDate" : "07-07-2023",
    "toDate" : "07-15-2023"
}</span>
</code></pre>

>>
Output:
>>>
    {
        "data": {
            "errorMessage": "",
            "traceback": "",
            "data": {
                "y": [
                    {
                        "date": "01-16-2022",
                        "counts": "[{\"tableCount\":22.3249225616,\"time\":11},{\"tableCount\":15.3308525085,\"time\":12},{\"tableCount\":6.0051803589,\"time\":13},{\"tableCount\":6.4271569252,\"time\":14},{\"tableCount\":3.3630287647,\"time\":15},{\"tableCount\":2.7648005486,\"time\":16},{\"tableCount\":5.4221305847,\"time\":17},{\"tableCount\":21.0307579041,\"time\":18},{\"tableCount\":17.9799308777,\"time\":19},{\"tableCount\":11.0987033844,\"time\":20},{\"tableCount\":7.7918105125,\"time\":21}]"
                    },
                    {
                        "date": "01-17-2022",
                        "counts": "[{\"tableCount\":4.3347301483,\"time\":11},{\"tableCount\":13.7139158249,\"time\":12},{\"tableCount\":22.5580196381,\"time\":13},{\"tableCount\":17.7829666138,\"time\":14},{\"tableCount\":10.4020938873,\"time\":15},{\"tableCount\":2.7406756878,\"time\":16},{\"tableCount\":4.4894299507,\"time\":17},{\"tableCount\":3.9393897057,\"time\":18},{\"tableCount\":2.5602560043,\"time\":19},{\"tableCount\":5.2975172997,\"time\":20},{\"tableCount\":24.4320220947,\"time\":21}]"
                    },
                    {
                        "date": "01-18-2022",
                        "counts": "[{\"tableCount\":25.5556297302,\"time\":11},{\"tableCount\":21.6066265106,\"time\":12},{\"tableCount\":16.9466266632,\"time\":13},{\"tableCount\":13.0571289062,\"time\":14},{\"tableCount\":22.881313324,\"time\":15},{\"tableCount\":34.0851211548,\"time\":16},{\"tableCount\":28.8900508881,\"time\":17},{\"tableCount\":23.1612758636,\"time\":18},{\"tableCount\":13.7236795425,\"time\":19},{\"tableCount\":12.1094703674,\"time\":20},{\"tableCount\":8.7841835022,\"time\":21}]"
                    },
                    {
                        "date": "01-19-2022",
                        "counts": "[{\"tableCount\":6.8754734993,\"time\":11},{\"tableCount\":9.8974742889,\"time\":12},{\"tableCount\":29.4479675293,\"time\":13},{\"tableCount\":33.2332077026,\"time\":14},{\"tableCount\":26.8839187622,\"time\":15},{\"tableCount\":22.5158405304,\"time\":16},{\"tableCount\":21.4588184357,\"time\":17},{\"tableCount\":31.3786964417,\"time\":18},{\"tableCount\":41.555103302,\"time\":19},{\"tableCount\":38.0847129822,\"time\":20},{\"tableCount\":33.7989006042,\"time\":21}]"
                    },
                    {
                        "date": "01-20-2022",
                        "counts": "[{\"tableCount\":21.2980632782,\"time\":11},{\"tableCount\":16.9026260376,\"time\":12},{\"tableCount\":9.3885774612,\"time\":13},{\"tableCount\":5.1352725029,\"time\":14},{\"tableCount\":8.3074045181,\"time\":15},{\"tableCount\":26.5341453552,\"time\":16},{\"tableCount\":32.1234817505,\"time\":17},{\"tableCount\":29.40417099,\"time\":18},{\"tableCount\":25.5267181396,\"time\":19},{\"tableCount\":18.9728393555,\"time\":20},{\"tableCount\":21.9795360565,\"time\":21}]"
                    },
                    {
                        "date": "01-21-2022",
                        "counts": "[{\"tableCount\":26.9185009003,\"time\":11},{\"tableCount\":23.7499847412,\"time\":12},{\"tableCount\":19.7978839874,\"time\":13},{\"tableCount\":10.8758878708,\"time\":14},{\"tableCount\":9.7679300308,\"time\":15},{\"tableCount\":4.2197132111,\"time\":16},{\"tableCount\":0.0849183798,\"time\":17},{\"tableCount\":2.3076190948,\"time\":18},{\"tableCount\":18.9048557281,\"time\":19},{\"tableCount\":22.7209529877,\"time\":20},{\"tableCount\":19.5034141541,\"time\":21}]"
                    },
                    {
                        "date": "01-22-2022",
                        "counts": "[{\"tableCount\":16.1986370087,\"time\":11},{\"tableCount\":9.5400733948,\"time\":12},{\"tableCount\":11.5875263214,\"time\":13},{\"tableCount\":16.3533973694,\"time\":14},{\"tableCount\":13.4710626602,\"time\":15},{\"tableCount\":9.5767259598,\"time\":16},{\"tableCount\":3.3179194927,\"time\":17},{\"tableCount\":6.832379818,\"time\":18},{\"tableCount\":5.7702031136,\"time\":19},{\"tableCount\":3.5545077324,\"time\":20},{\"tableCount\":4.9158325195,\"time\":21}]"
                    }
                ],
                "x": "",
                "note": "predicting without explanation"
            }
        }
    }
<br>
<br>

<!-- ### predict_link

<u>Method Details :</u>

>
This method is used to get prediction of next item iteration.
>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.
>>
<u>Payload :</u>
>>>
    "functionName": "predict_link"
>>>>
It is the function name to identify request.
>>>
    panel: ObjectId
>>>>                                                
It is the object id of custom panel widget of which you want to get prediction.
>>>
    model: String
>>>>                                                
It is the  model key which you want to get prediction.
>>>
    fromDate :date
>>>>
It is the date of dataset in pipeline from which model will create.
>>>
    toDate : Date
>>>>
It is the date of dataset in pipeline to which model will create. 
>>>
    guestCount : Number
>>>>
It is the number of question count to get prediction.
>>>
    dimItems : Array
>>>>
It is the array consist of items.

>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "predict_link",
    "panel" : '648171758ae9ce41584b8d02',
    "model" : '649fd6065ad0c04e52902ecb',
    "fromDate" : "07-07-2023",
    "toDate" : "07-15-2023",
    "guestCount" :4,
    "dimItems" : [   
        "MOZZARELLA STICKS",
        "BBQ BRISKET CHIPS",
        "ROOT BREWSKI FLOAT"
    ]
}</span>
</code></pre>

>>
Output:
>>
    {
        "data": {
            "note": "shape is (output times, output names, input times                ) which means (slider value 1-77, output dropdown which is only 1 this time ==tablecount,               input times == 1 which I think we should just average)",
            "x": "",
            "y": [
                {
                    "counts": "[{\"tableCount\":24.3177656418,\"time\":22},{\"tableCount\":22.5132884603,\"time\":23}]",
                    "date": "01-10-2022"
                },
                {
                    "counts": "[{\"tableCount\":11.4887220234,\"time\":11},{\"tableCount\":0.9871529177,\"time\":12},{\"tableCount\":-4.3497954395,\"time\":13},{\"tableCount\":-3.9493748949,\"time\":14},{\"tableCount\":-1.7526181655,\"time\":15},{\"tableCount\":-1.4439894611,\"time\":16},{\"tableCount\":-1.0401968262,\"time\":17},{\"tableCount\":-1.0844750324,\"time\":18},{\"tableCount\":-1.5875342641,\"time\":19},{\"tableCount\":-1.650071388,\"time\":20},{\"tableCount\":-0.4756426904,\"time\":21},{\"tableCount\":-1.5778256151,\"time\":22},{\"tableCount\":-1.7702295068,\"time\":23}]",
                    "date": "01-11-2022"
                },
                {
                    "counts": "[{\"tableCount\":2.6188565342,\"time\":11},{\"tableCount\":0.5729791225,\"time\":12},{\"tableCount\":-0.417372317,\"time\":13},{\"tableCount\":18.7773222981,\"time\":14},{\"tableCount\":24.7967677937,\"time\":15},{\"tableCount\":19.655833873,\"time\":16},{\"tableCount\":12.0238078291,\"time\":17},{\"tableCount\":9.0015940878,\"time\":18},{\"tableCount\":16.6094565211,\"time\":19},{\"tableCount\":31.5952245877,\"time\":20},{\"tableCount\":34.0088619296,\"time\":21},{\"tableCount\":22.729224439,\"time\":22},{\"tableCount\":10.4766759527,\"time\":23}]",
                    "date": "01-12-2022"
                },
                {
                    "counts": "[{\"tableCount\":2.4063534054,\"time\":11},{\"tableCount\":-1.3046558475,\"time\":12},{\"tableCount\":-1.5467832831,\"time\":13},{\"tableCount\":-1.5026270867,\"time\":14},{\"tableCount\":-1.7404576518,\"time\":15},{\"tableCount\":-1.1224250781,\"time\":16},{\"tableCount\":-0.4942754908,\"time\":17},{\"tableCount\":-0.5818096361,\"time\":18},{\"tableCount\":-0.4196951604,\"time\":19},{\"tableCount\":-1.6465237508,\"time\":20},{\"tableCount\":-2.7857182719,\"time\":21},{\"tableCount\":1.5850515717,\"time\":22},{\"tableCount\":0.0179848449,\"time\":23}]",
                    "date": "01-13-2022"
                },
                {
                    "counts": "[{\"tableCount\":1.2416835429,\"time\":11},{\"tableCount\":24.6564399511,\"time\":12},{\"tableCount\":31.9739965184,\"time\":13},{\"tableCount\":27.4041761928,\"time\":14},{\"tableCount\":23.7017095304,\"time\":15},{\"tableCount\":19.2836633571,\"time\":16},{\"tableCount\":25.7184772204,\"time\":17},{\"tableCount\":37.4876653524,\"time\":18},{\"tableCount\":39.3026513758,\"time\":19},{\"tableCount\":27.5750012111,\"time\":20},{\"tableCount\":15.5525586614,\"time\":21},{\"tableCount\":8.7555330587,\"time\":22},{\"tableCount\":0.789612545,\"time\":23}]",
                    "date": "01-14-2022"
                },
                {
                    "counts": "[{\"tableCount\":-1.1087360365,\"time\":11},{\"tableCount\":-2.2519836383,\"time\":12},{\"tableCount\":-3.4695554996,\"time\":13},{\"tableCount\":-1.7532479032,\"time\":14},{\"tableCount\":-0.9624333285,\"time\":15},{\"tableCount\":-0.1002330354,\"time\":16},{\"tableCount\":0.2011530268,\"time\":17},{\"tableCount\":-0.990910253,\"time\":18},{\"tableCount\":-2.0095834439,\"time\":19},{\"tableCount\":1.6610809827,\"time\":20},{\"tableCount\":-0.1798172856,\"time\":21},{\"tableCount\":-0.4944439009,\"time\":22},{\"tableCount\":20.692877,\"time\":23}]",
                    "date": "01-15-2022"
                },
                {
                    "counts": "[{\"tableCount\":30.013893362,\"time\":11},{\"tableCount\":26.1200715596,\"time\":12},{\"tableCount\":21.4959226514,\"time\":13},{\"tableCount\":15.7068853822,\"time\":14},{\"tableCount\":17.8399456008,\"time\":15},{\"tableCount\":26.2775138224,\"time\":16},{\"tableCount\":23.6347543563,\"time\":17},{\"tableCount\":14.2409703754,\"time\":18},{\"tableCount\":5.3022626512,\"time\":19},{\"tableCount\":0.5790530883,\"time\":20}]",
                    "date": "01-16-2022"
                }
            ]
        },
        "errorMessage": "",
        "traceback": ""
    }
<br>
<br> -->

### explain_link

<u>Method Details :</u>

>
This method is used to get explanability values of of next link.
>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.
>>
<u>Payload :</u>
>>>
    "functionName": "explain_link"
>>>>
It is the function name to identify request.
>>>
    model: String
>>>>
It is the object id of custom panel widget of which you want to get prediction.
>>>
    config: Object
>>>>
It is Object consts of seedNodeNameCol, prediction, seedNodeNames, refNodeDict keys.
>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
  "functionName": "explain_link",
  "model": "MODEL KEY",
  "config": {
    "seedNodeNameCol": "ItemDescription",
    "prediction": 10,
    "seedNodeNames": [
      "1",
      "2"
    ],
    "refNodeDict": {
      "GuestCount": 0,
      "CheckOpen": "2023-09-08T05:14:05.283Z"
    }
  }
}</span>
</code></pre>
<br>
<br>

### predict_time

<u>Method Details :</u>

>
This method is used to get prediction of table count.
>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.
>>
<u>Payload :</u>
>>>
    "functionName": "predict_time"
>>>>
It is the function name to identify request.
>>>
    panel: ObjectId
>>>>
It is the object id of custom panel widget of which you want to get prediction.
>>>
    model: String
>>>>
It is the  model key which you want to get prediction.
>>>
    fromDate :Date
>>>>
It is the date of dataset in pipeline from which model will create.
>>>
    toDate : Date
>>>>
It is the date of dataset in pipeline to which model will create.
>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "predict_time",
    "panel" : "PANEL_ID",
    "model" : "MODEL_ID",
    "fromDate" : "07-07-2023",
    "toDate" : "07-15-2023"
}</span>
</code></pre>
>>
Output:
>>
  <pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">  {
        "data": {
            "note": "shape is (output times, output names, input times ) which means (slider value 1-77, output dropdown which is only 1 this time ==tablecount,input times == 1 which I think we should just average)",
            "x": "",
            "y": [
                {
                    "counts": "[{\"tableCount\":24.3177656418,\"time\":22},{\"tableCount\":22.5132884603,\"time\":23}]",
                    "date": "01-10-2022"
                }
            ]
        },
        "errorMessage": "",
        "traceback": ""
    }</span>
</code></pre>

<br>
<br>

### predict_next_link

<u>Method Details :</u>

>
This method is used to get prediction of next link model.
>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.
>>
<u>Payload :</u>
>>>
    "functionName": "predict_next_link"
>>>>
It is the function name to identify request.
>>>
    model: String
>>>>
It is the object id of custom panel widget of which you want to get prediction.
>>>
    config: Object
>>>>
It is Object consts of seedNodeNameCol, prediction, seedNodeNames, refNodeDict keys.
>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
  "functionName": "predict_next_link",
  "model": "MODEL KEY",
  "config": {
    "seedNodeNameCol": "ItemDescription",
    "prediction": 10,
    "seedNodeNames": [
      "1",
      "2"
    ],
    "refNodeDict": {
      "GuestCount": 0,
      "CheckOpen": "2023-09-08T05:14:05.283Z"
    }
  }
}</span>
</code></pre>
<br>
<br>

### train_mixed

<u>Method Details :</u>

>
This method is used to train model with timeseries off for provided user's pipeline.
>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.
>>
<u>Payload :</u>
>>>
    "functionName": "train_mixed"
>>>>
It is the function name to identify request.
>>>
    title  : "MODEL_NAME"
>>>>
It is the name of model you want to give.
>>>
    fromDate :Date
>>>>
It is the date of dataset in pipeline from which model will create.
>>>
    toDate : Date
>>>>
It is the date of dataset in pipeline to which model will create.
>>>
    "table" : "TABLE_NAME"
>>>>
It is name of table of which you want to consider while creating model.
>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "train_mixed",
    "title"  : "MODEL_NAME",
    "fromDate" :"07-07-2023",
    "toDate" : "07-15-2023",
    "table" : "Table name"
}</span>
</code></pre>

>>
Output:
>>
   <pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
        'status': 'In progress',
        'model Id': 'MDOEL ID',
        'apiKey': 'MODEL KEY'
    }</span>
</code></pre>

<br>
<br>

### train_timeseries

<u>Method Details :</u>

>
This method is used to train model with timeseries on for provided user's pipeline.

>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.
>>
<u>Payload :</u>
>>>
    "functionName": "train_timeseries"
>>>>
It is the function name to identify request.
>>>
    title  : "MODEL_NAME"
>>>>
It is the name of model you want to give.
>>>
    fromDate :Date
>>>>
It is the date of dataset in pipeline from which model will create.
>>>
    toDate : Date
>>>>
It is the date of dataset in pipeline to which model will create.
>>>
    "table" : "TABLE_NAME"
>>>>
It is name of table of which you want to consider while creating model.
>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "train_timeseries",
    "title"  : "MODEL_NAME",
    "fromDate" :"07-07-2023",
    "toDate" : "07-15-2023",
    "table" : "Table name"
}</span>
</code></pre>

>>
Output:
>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">   {
        'status': 'In progress',
        'model Id': 'MDOEL ID',
        'apiKey': 'MODEL KEY'
    }</span>
</code></pre>

### next_link

<u>Method Details :</u>

>
This method is used to create model next link type.

>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.
>>
<u>Payload :</u>
>>>
    "functionName": "next_link"
>>>>
It is the function name to identify request.
>>>
    title  : "MODEL_NAME"
>>>>
It is the name of model you want to give.
>>>
    settings :Oobject
>>>>
It is object consist of dates, trainNodeType, dummyNodeType and seedNodeType keys.
>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "train_timeseries",
    "title"  : "MODEL_NAME",
    "settings" :   {
        "dates": {
            "dim_item": {
            "from": "01-01-2023",
            "to": "12-31-2023",
            "allDate": false
            },
            "check": {
            "from": "01-01-2023",
            "to": "12-31-2023",
            "allDate": false
            },
            "check_item": {
            "from": "01-01-2023",
            "to": "12-31-2023",
            "allDate": false
            }
        },
        "trainNodeType": "check",
        "dummyNodeType": "check",
        "seedNodeType": "dim_item"
    }
}</span>
</code></pre>

>>
Output:
>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">
   {
        'status': 'In progress',
        'model Id': 'MDOEL ID',
        'apiKey': 'MODEL KEY'
    }</span>
</code></pre>

<br>
<br>

### delete_model

<u>Method Details :</u>

>
This method is used to create model next link type.

>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.
>>
<u>Payload :</u>
>>>
    "functionName": "delete_model"
>>>>
It is the function name to identify request.
>>>
    model  : "MODEL_KEY"
>>>>
Model unique id to identify the pipeline in our platform.

>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "delete_model",
    "model" : 'MODEL_KEY'
}</span>
</code></pre>

>>
Output:
>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    success : true,
    message : 'Model deleted successfully.'
}</span>
</code></pre>

<br>
<br>

### retrain_model

<u>Method Details :</u>

>
This method is used to retrain model same as from UI.

>>
<u>Header :</u>
>>>
    "user-secret": "USER_SECRET"
>>>>
User unique id to identify the user in our platform.
>>>
    "pipeline": "PIPELINE_KEY"
>>>>
Pipeline unique id to identify the pipeline in our platform.
>>
<u>Payload :</u>
>>>
    "functionName": "retrain_model"
>>>>
It is the function name to identify request.
>>>
    model  : "MODEL_KEY"
>>>>
Model unique id to identify the pipeline in our platform.

>>
Example's argument:
>>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "functionName": "retrain_model",
    "model" : 'MODEL_KEY'
}</span>
</code></pre>

>>
Output:
>>
<pre class="content-block ml-40"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
  "success": true,
  "message": "Model retrained successfully",
  "title": "TITLE OF NEW TRAINED MODEL"
}</span>
</code></pre>

<br>
<br>
<br>

<script src="./script.js"></script>
