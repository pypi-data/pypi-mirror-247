from vai_toolkit.client import *
import json


def create(user_secret, title, type) -> object:
    """This method is used to create pipeline of provided user. 
    
    args:

        user_secret {string}: It is the user secret key.
        title {string}: It is the name of pipeline to assign.
        type {string}: It is the type of pipeline. it could be only 'TABULAR' or 'GRAPH'

    returns: 

        type: Created pipeline response object.

    Example:

        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import pipeline

        title  = "Tabular data"
        type = "TABULAR"
        user_secret  =  'USER_SECRET_KEY'

        res = pipeline.create(user_secret, title, type)
        print(res)
        </span>
        </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
            '_id': '65017bdc104c04cd9663ba05', 
            'title': 'Tabular data', 
            'apiKey': 'd2159682-aecc-49cf-ba7d-a8bfcc828d5e-1694596060912'
        }</span>
        </code></pre>
    """

    headers =create_headers(user_secret)
    
    payload =json.dumps({
            "functionName": "create_pipeline",
            "title": title,   
            "type": type, 
        })
    
    return validate_response(payload,headers)
     
def list_alerts(user_secret, pipeline_key) -> list:
    """This method is used to get the list of alerts for given pipeline of user.
    
    args:

        user_secret {string}: It is the user secret key.
        pipeline_key {string}: It is the pipeline key.

    returns: 

        type: List of all alerts objects.

    Example:
    
        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import pipeline

        user_secret  =  'USER_SECRET_KEY'
        pipeline_key =  'PIPELINE_KEY'

        res = pipeline.list_alerts(user_secret, pipeline_key)
        print(res)
        </span>
        </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">[
            {
                'timeWindow': {
                    'window': None, 
                    'startTime': None, 
                    'endTime': None, 
                    'column': None, 
                    'dates': [], 
                    'times': [], 
                    'isHoliday': None, 
                    'holidays': [], 
                    'step': None
                    }, 
                    '_id': '65017d26104c04cd9663c23e', 
                    'name': 'test', 
                    'type': 'DATASET', 
                    'pipelineId': '65017bdc104c04cd9663ba05', 
                    'modelId': None, 
                    'creator': '62c56baeb4fbc200139daed0', 
                    'from': '1/1/2023', 
                    'to': '12/31/2023', 
                    'columnFields': ['race', 'hours-per-week', 'age'], 
                    'week': 2, 
                    'thresholdLimit': 49, 
                    'createdAt': '2023-09-13T09:13:10.080Z', 
                    'updatedAt': '2023-09-13T09:13:10.080Z'
            }
        ]
        </span>
        </code></pre>
    """

    headers =create_headers(user_secret, pipeline = pipeline_key)

    payload = json.dumps({
            "functionName": "list_alerts",
        })

    return validate_response(payload,headers)

def create_alert(user_secret, pipeline_key, settings) -> object:
    """This method is used to create alert for given pipeline of user.
    args:

        user_secret {string}: It is the user secret key.
        pipeline_key {string}: It is the pipeline key.
        settings {obj}: It is data object to create alerts.

    returns: 

        type: Created alert response object.

    Example:

        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import pipeline

        user_secret  =  'USER_SECRET_KEY'
        pipeline_key =  'PIPELINE_KEY'
        data ={
            "name":"test",
            "type":"DATASET",
            "from": "1/1/2023", 
            "to": "12/31/2023",
            "columnFields": ["race",  "hours-per-week", "age"],
            "week": 2,  
            "thresholdLimit": 49
        }

        res = pipeline.create_alert(user_secret, pipeline_key ,data)
        print(res)
        </span>
        </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
            'name': 'test', 
            'type': 'DATASET', 
            'pipelineId': '65017bdc104c04cd9663ba05', 
            'modelId': None, 
            'creator': '62c56baeb4fbc200139daed0', 
            'from': '1/1/2023', 
            'to': '12/31/2023', 
            'columnFields': ['race', 'hours-per-week', 'age'], 
            'week': 2, 
            'thresholdLimit': 49, 
            'timeWindow': {
                'window': None, 
                'startTime': None, 
                'endTime': None, 
                'column': None, 
                'dates': [], 
                'times': [], 
                'isHoliday': None, 
                'holidays': [], 
                'step': None
            }, 
            'createdAt': '2023-09-13T09:13:10.080Z', 
            'updatedAt': '2023-09-13T09:13:10.080Z', 
            '_id': '65017d26104c04cd9663c23e'}
        </span>
        </code></pre>
    """

    headers =create_headers(user_secret, pipeline = pipeline_key)

    payload = json.dumps({
            "functionName": "create_alert",
            "data": settings
        })

    return validate_response(payload,headers)


def create_table(user_secret, pipeline_key, name ) ->object:
    """This method is used to create table for given pipeline of user.

    args:

            user_secret {string}: It is the user secret key.
            pipeline_key {string}: It is the pipeline key.
            name {string}: It is the name of table.

    returns: 

            type: Created alert response object.
    Example:

            <pre class="content-block ml-20"><div class="copy-button">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
            <div class="copy-text"></div>
            </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import pipeline

            user_secret  =  'USER_SECRET_KEY'
            pipeline_key =  'PIPELINE_KEY'
            name = 'TABLE NAME'

            res = pipeline.create_table(user_secret, pipeline_key ,data)
            print(res)
            </span>
            </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
                'success': True,
                'table': {'name': 'Table Name','pipeline': 'Pipeline id', '_id': 'Table Id'}
            }
        </span>
        </code></pre>
        """
    headers =create_headers(user_secret, pipeline = pipeline_key)

    payload = json.dumps({
            "functionName": "create_table",
            "name": name
        })

    return validate_response(payload,headers)


def update_table(user_secret, pipeline_key,old_name, new_name ) ->str:
    """This method is used to update table name for given pipeline of user.

    args:

            user_secret {string}: It is the user secret key.
            pipeline_key {string}: It is the pipeline key.
            old_name {string}: It is the name of current name of table.
            new_name {string}: It is the new name of table to update.

    returns: 

            type: Created alert response object.
    Example:

            <pre class="content-block ml-20"><div class="copy-button">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
            <div class="copy-text"></div>
            </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import pipeline

            user_secret  =  'USER_SECRET_KEY'
            pipeline_key =  'PIPELINE_KEY'
            old_name = 'TABLE NAME'
            new_name = 'NEW TABLE NAME'

            res = pipeline.update_table(user_secret, pipeline_key ,old_name, new_name)
            print(res)
            </span>
            </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">Name updated successfully.
        </span>
        </code></pre>
        """
    headers =create_headers(user_secret, pipeline = pipeline_key)

    payload = json.dumps({
            "functionName": "update_table",
            "oldName": old_name,
            "newName": new_name
        })

    return validate_response(payload,headers)

def get_table(user_secret, pipeline_key )  ->object:
    """This method is used to get tables of given pipeline of user.

    args:

            user_secret {string}: It is the user secret key.
            pipeline_key {string}: It is the pipeline key.

    returns: 

            type: Created alert response object.
    Example:

            <pre class="content-block ml-20"><div class="copy-button">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
            <div class="copy-text"></div>
            </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import pipeline

            user_secret  =  'USER_SECRET_KEY'
            pipeline_key =  'PIPELINE_KEY'

            res = pipeline.get_table(user_secret, pipeline_key )
            print(res)
            </span>
            </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">[
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
        </span>
        </code></pre>
            """
    headers =create_headers(user_secret, pipeline = pipeline_key)

    payload = json.dumps({
            "functionName": "get_table",
        })

    return validate_response(payload,headers)


def delete_table(user_secret, pipeline_key, name )  ->str:
    """This method is used to delete table for given pipeline of user.

    args:

            user_secret {string}: It is the user secret key.
            pipeline_key {string}: It is the pipeline key.
            name {string}: It is the name of table.

    returns: 

            type: Created alert response object.
    Example:

            <pre class="content-block ml-20"><div class="copy-button">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
            <div class="copy-text"></div>
            </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import pipeline

            user_secret  =  'USER_SECRET_KEY'
            pipeline_key =  'PIPELINE_KEY'
            name = 'TABLE NAME TO DELETE'

            res = pipeline.delete_table(user_secret, pipeline_key ,name)
            print(res)
            </span>
            </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">Table deleted successfully.
            
        </span>
        </code></pre>"""
    headers =create_headers(user_secret, pipeline = pipeline_key)

    payload = json.dumps({
            "functionName": "delete_table",
            "name": name
        })

    return validate_response(payload,headers)

def set_default_table(user_secret, pipeline_key, name )  ->str:
    """This method is used to set default table for given pipeline of user.

    args:

            user_secret {string}: It is the user secret key.
            pipeline_key {string}: It is the pipeline key.
            name {string}: It is the name of table.

    returns: 

            type: Created alert response object.
    Example:

            <pre class="content-block ml-20"><div class="copy-button">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
            <div class="copy-text"></div>
            </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import pipeline

            user_secret  =  'USER_SECRET_KEY'
            pipeline_key =  'PIPELINE_KEY'
            name = 'TABLE NAME TO SET DEFAULT'

            res = pipeline.set_default_table(user_secret, pipeline_key ,name)
            print(res)
            </span>
            </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">Default table successfully.
            
        </span>
        </code></pre>"""
    headers =create_headers(user_secret, pipeline = pipeline_key)

    payload = json.dumps({
            "functionName": "set_default_table",
            "name": name
        })

    return validate_response(payload,headers)


def delete_pipeline(user_secret, pipeline_key)  ->object:
    """This method is used to delete pipeline when there is no dataset in pipeline

    args:

            user_secret {string}: It is the user secret key.
            pipeline_key {string}: It is the pipeline key.

    returns: 

            type: Created alert response object.
    Example:

            <pre class="content-block ml-20"><div class="copy-button">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
            <div class="copy-text"></div>
            </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import pipeline

            user_secret  =  'USER_SECRET_KEY'
            pipeline_key =  'PIPELINE_KEY'

            res = pipeline.delete_pipeline(user_secret, pipeline_key )
            print(res)
            </span>
            </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
                message: "Pipeline deleted successfully!.."
        }
        </span>
        </code></pre>
            """
    headers =create_headers(user_secret, pipeline = pipeline_key)

    payload = json.dumps({
            "functionName": "delete_pipeline",
    })

    return validate_response(payload,headers)