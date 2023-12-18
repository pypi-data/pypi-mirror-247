from vai_toolkit.client import *
import json


def download_csvs(user_secret, pipeline_key, to_file, from_date="", to_date="", table_name = '') -> object:
    """This method is used to download dataset for given pipeline and table of user.
    
    args:

        user_secret {string}: It is the user secret key.
        pipeline_key {string}: It is the pipeline key.
        to_file {string}: It is file path in which store all csvs.
        from_date {string}: It is from date value in 'MM-DD-YYYY' format.
        to_date {string}: It is to date value in 'MM-DD-YYYY' format.
        table_name {string}: It is name of table to download data.

    returns: 

        type: Response message.

    Example:

        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import data

        user_secret  =  'USER_SECRET_KEY'
        pipeline_key =  'PIPELINE_KEY'
        from_date = "09/01/2023" # From Date
        to_date = "09/11/2023" # From Date
        path = "./new2.zip" #Path
        table='Table 2'

        res = data.download_csvs(user_secret, pipeline_key, path, from_date=from_date, to_date=to_date,table_name=table)

        print(res)
        </span>
        </code></pre>
    """

    try:

        headers =create_headers(user_secret, pipeline= pipeline_key)
        payload = json.dumps({
            "functionName": "download_csvs",
            "fromDate": from_date,
            "table":table_name,
            "toDate": to_date
        })  
        response = validate_response_download(payload,headers )
        if(response.status_code == 200) :
            f = open(to_file, 'wb')
            f.write(response.content)
            f.close()
            return "File saved successfully"
        else :
            response = json.loads(response.text)
            if ('message' in response):
                return  (response['message'])
            else :
                return response
    except Exception as e:
        return e
    
def list_labels(user_secret, pipeline_key, table_name = '') -> object:
    """This method is used to get labels for given pipeline and table of user. 

    args:

        user_secret {string}: It is the user secret key.
        pipeline_key {string}: It is the pipeline key.
        table_name {string}: It is name of table to download data.

    returns: 

        type: List of all labels.

    Example:

        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import data

        user_secret  =  'USER_SECRET_KEY'
        pipeline_key =  'PIPELINE_KEY'

        table_name = 'Table 2'
        res = data.list_labels(user_secret, pipeline_key,table_name =table_name  )

        print(res)
        </span>
        </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
            'success': True, 
            'details': {
                'Table Name': 'Table 2', 
                'Column Names': ['id', 'Capital Gain'], 
                'Column Types': ['CATEGORY', 'CATEGORY'], 
                'Column Labels': [None, None]
            }
        }
        </span>
        </code></pre>
    """
    
    headers =create_headers(user_secret, pipeline= pipeline_key) 
    payload = json.dumps({ 
            "functionName": "list_labels",
            "table": table_name
        })
    return validate_response(payload,headers)

def set_labels(user_secret, pipeline_key, labels, d_types, table_name = '') -> object:
    """This method is used to set labels for given pipeline and table of user. 
    
    args:

        user_secret {string}: It is the user secret key.
        pipeline_key {string}: It is the pipeline key.
        labels {object} : It is dictionary containing the keys as the column of provided pipeline and values are Input, Protected and Output of that column as column label.
        d_types {object}: It is dictionary containing the keys as the column of provided pipeline and values are NUMBER, STRING, and CATEGORICAL of that column as column type.
        table_name {string}: It is name of table to download data.

    returns: 

        type: Get response with added labels.

    Example:

        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import data

        user_secret  =  'USER_SECRET_KEY'
        pipeline_key =  'PIPELINE_KEY'
        columnLabels = { "id" : 'Input' ,"Capital Gain" : 'Output'  } # Column Labels
        columnTypes ={ "id" : 'CATEGORY',"Capital Gain" : 'CATEGORY' } # Column Types
        table_name = 'Table 2'

        res = data.set_labels(user_secret, pipeline_key, columnLabels, columnTypes,table_name)
        print(res)
        </span>
        </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
            'tableName': 'dim_item',
            'columnLabels': [None, 'Output', None, None, 'Input', None, None, None, None],
            'columnNames': ['A1', 'DimItemkey', 'RestaurantCustomerName', 'PLU', 'ItemDescription', 'ItemSubcategory', 'ItemCategory', 'ItemReportingCategory', 'ItemFNBCategory'],
            'columnTypes': ['CATEGORY', 'CATEGORY', 'CATEGORY', 'CATEGORY', 'STRING', 'CATEGORY', 'CATEGORY', 'CATEGORY', 'CATEGORY'],
            'pipeline': 'pipeline id',
            '_id': 'Table id'
        }</span></code></pre>
    """
    
    headers =create_headers(user_secret, pipeline= pipeline_key) 
    payload = json.dumps({ 
            "functionName": "set_labels",
                "columnLabels": labels,
                "columnTypes": d_types,
                "table" : table_name
        })
    return validate_response(payload,headers)

def upload_data(user_secret, pipeline_key, data, date, time, new_columns=False, duplicates=False, new_categories=False, table_name = '') -> object:
    """This method is used to upload data for given pipeline and table of user. 
    
    args:

        user_secret {string}: It is the user secret key.
        pipeline_key {string}: It is the pipeline key.
        data {obj}: It is data object to upload data.
        date {array}: It is list of dates value in 'MM-DD-YYYY' format.
        time {array}: It is list of time value in 'HH:MM:SS' format.
        new_columns {boolean}: It is boolean value for add new columns either 'True' or 'False'.
        duplicates {boolean}: It is boolean value either 'True' or 'False'.
        new_categories {boolean}: It is boolean value for add new categories either 'True' or 'False'.
        table_name {string}: It is name of table.

    returns: 

        type: Uploaded data object in response.

    Example:

        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import data

        user_secret  =  'USER_SECRET_KEY'
        pipeline_key =  'PIPELINE_KEY'
        uploadData = { "id": [11111, 1], "Capital Gain": [10000, 15000] }   # Columns data
        dates = ["09-06-2023", "09-06-2023"]  # Dates
        times = ["11:08:50", "11:09:50" ]  # Times
        table_name =  'Table 2'

        res = data.upload_data(user_secret, pipeline_key, uploadData, dates, times, new_columns = True, duplicates = True,new_categories =  True ,table_name=table_name)
        print(res)
        </span>
        </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
            'success': True, 
            'data': '{
                "dates":["09-06-2023"]
            }', 
            'warning': 'We insert the duplicate data if we found.'}
        </span>
        </code></pre>
    """

    headers =create_headers(user_secret, pipeline= pipeline_key)  
    payload = json.dumps({ 
        "functionName": "upload_data",
        "date": date,
        "time" : time,
        "data" : data,
        "allowNewColumns" : new_columns,
        "allowDuplicate" : duplicates,
        "allowNewCategory" : new_categories,
        "table":table_name
        })   
    return validate_response(payload,headers)

def upload_csv(user_secret, pipeline_key, path, table_name ) -> object:
    """This method is used to upload csv for given pipeline and table of user. 
    
    args:

        user_secret {string}: It is the user secret key.
        pipeline_key {string}: It is the pipeline key.
        path {string}: It is the path value of csv file.
        table_name {string}: It is name of table in which you want to upload.

    returns: 

        type: Response message.

    Example:

        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import data

        user_secret  =  'USER_SECRET_KEY'
        pipeline_key =  'PIPELINE_KEY'
        table_name = 'Table 1'

        res = data.upload_csv(user_secret, pipeline_key, "./09-11-2023.csv", table_name)
        print(res)
        </span>
        </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">Dataset uploaded succesfully.
        </span>
        </code></pre>
    """

    headers =create_headers(user_secret, pipeline= pipeline_key)  
    return validate_response_upload('upload_csv' ,path, table_name,headers)

def set_relations(user_secret, pipeline_key, primary_keys_obj, to_table, relation_array) -> object:
    """This method is used to set relations between tables of given pipeline of user.
    
    args:

        user_secret {string}: It is the user secret key.
        pipeline_key {string}: It is the pipeline key.
        primary_keys_obj {string}: It is an object where key represents the name of table, and it's value is considered as primary key column.
        to_table {string}: It is the table name of which you want to set main table to bind other tables.
        relation_array {array}: It is an array consists of relation object, where object is { "from":"From table name",  "toColumn": "Where column of to table want to bind"}.

    returns: 

        type: Get response message

    Example:

        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import data

        user_secret  =  'USER_SECRET_KEY'
        pipeline_key =  'PIPELINE_KEY'
        primary_keys_obj = {
            "dim_item": "PLU",
            "check": "CheckKey",
            "check_item": "CheckItemKey"
        }
        to_table =  "check_item"
        relation_array =  [
            {
                "from": "dim_item",
                "toColumn": "ItemNumber"
            },
            {
                "from": "check",
                "toColumn": "CheckKey"
            }
        ]
        res = data.set_relations(user_secret, pipeline_key, primary_keys_obj, to_table, relation_array)

        print(res)
        </span>
        </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
            "message": "Updated successfully."
        }</span>
        </code></pre>
    """

    try:
        headers =create_headers(user_secret,pipeline= pipeline_key)  
        payload = json.dumps({ 
            "functionName": "set_relations",
            "primaryKeys": primary_keys_obj,
            "toTable" : to_table,
            "relations" : relation_array,
        })   
        return validate_response(payload,headers)
    except Exception as e:
        return e
    

def delete_data(user_secret, pipeline_key, from_date, to_date, table_name = '') -> object:
    """This method is used to delete dataset data for given range in pipeline of user.
    
    args:

        user_secret {string}: It is the user secret key.
        pipeline_key {string}: It is the pipeline key.
        from_date {string}: It is from date value in 'MM-DD-YYYY' format.
        to_date {string}: It is to date value in 'MM-DD-YYYY' format.
        table_name {string}: It is name of table to delete data.

    returns: 

        type: Get response message

    Example:

        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import data

        user_secret  =  'USER_SECRET_KEY'
        pipeline_key =  'PIPELINE_KEY'
        from_date = "09/06/2023" # From Date
        to_date = "09/06/2023" # From Date
        table='Table 2'

        res = data.delete_data(user_secret, pipeline_key,  from_date, to_date, table )

        print(res)
        </span>
        </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
            "message": "Deleted successfully!.."
        }</span>
        </code></pre>
    """
    try:
        headers =create_headers(user_secret,pipeline= pipeline_key)  
        payload = json.dumps({ 
            "functionName": "delete_data",
            "fromDate": from_date,
            "toDate" : to_date,
            "table" : table_name,
        })   
        return validate_response(payload,headers)
    except Exception as e:
        return e