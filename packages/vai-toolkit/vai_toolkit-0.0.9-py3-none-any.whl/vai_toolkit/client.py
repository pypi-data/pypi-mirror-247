# TODO: finish get all payloads to work ()
# ASSUME: fromDate toDate (both empty means all, from date means all after, to date means all before)

import requests, json 
import time

url = "https://dev-cloud-api.virtuousai.com/vai-toolkit"
url_upload = "https://dev-data.virtuousai.com/data/upload_data"

# url = "https://cloud-api.virtuousai.com/vai-toolkit"
# url_upload = "https://data.virtuousai.com/data/upload_data"


def update_password(user_secret, new_password) -> object:
    """This method is used to update user password.
    
    args:

        user_secret {string}: It is the user secret key.
        new_password {string}: User new password value

    returns:

        type: Response object.

    Example:

        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import client 
        user_secret = 'USER_SECRET_KEY'
        new_password = 'NEW_SECURE_PASSWORD'

        res = client.update_password(user_secret, password)

        print(res)

        </span>
        </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
            "message": "Password changed successfully!.."
        }</span>
        </code></pre>
        
    """

    headers =create_headers(user_secret)
    if(headers):
        payload =json.dumps({
                "functionName":"update_password", 
                "password" : new_password
        })
        return validate_response(payload, headers=headers)
    else:
         return {"success": False , "message" :"Invalid Connection"}

def update_name(user_secret, first_name, last_name) -> object:
    """This method is used to update user's first name and last name. 
    
    args:

        user_secret {string}: It is the user secret key.
        first_name {string}: User first name value
        last_name {string}: User last name value

    returns:

        type: User object with updated name.

    Example:

        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import client 

        user_secret = 'USER_SECRET_KEY'
        first_name = 'John'
        last_name = 'Deo'

        updated_pass = client.update_name(user_secret ,first_name ,last_name )
        print(updated_pass)

        </span>
        </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
            "email": "john.deo@gmail.com",
            "_id": "61efccd707170700131a87c2",
            "firstName": "John",
            "lastName": "Deo",
        }</span>
        </code></pre>
    """

    try:
        headers =create_headers(user_secret)
        payload =json.dumps({
                "functionName":"update_name", 
                "firstName": first_name, 
                "lastName": last_name
        })
        return validate_response(payload, headers=headers)
    except Exception as e:
        return e

def create_account( email ,password, firstname ,lastname):
    # """CREATE A NEW ORGANIZATION"""
    payload =json.dumps({
            "functionName":"create_account",
             "email" :email ,
             "password" :password , 
             "firstName" :firstname ,
             "lastName" :lastname
        })

    return validate_response(payload, headers={})

def create_organization(user_secret, name, users) -> object:
    """This method is used to create organization for user.
    
    args:

        user_secret {string}: It is the user secret key.
        name {string}: It is name of organization to create
        users {obj}: It is the object consisting of keys as the emails and values as the role to be assigned to that specific email. Eg., { "john.deo@gmail.com" :"ADMIN" }
    
    returns:

        type: Created organization object.

    Example:

        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import client 

        org_name  = "ORGANIZATION_NAME"
        users = { 'john.deo@gmail.com' : 'ADMIN' }
        user_secret = 'USER_SECRET_KEY'

        res = client.create_organization(user_secret, org_name, users)
        print(res)
        </span>
        </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
            "user": "61efccd707170700131a87v2",
            "name": "ORGANIZATION_NAME",
            "datasetS3TotalSize": 0,
            "isDeleted": false,
            "createdAt": "2023-07-19T05:34:13.391Z",
            "updatedAt": "2023-07-19T05:34:13.391Z",
            "_id": "64b775d5f0a90246a2a2c31cd"
        }</span>
        </code></pre>
    """

    headers =create_headers(user_secret)
    payload =json.dumps({
            "functionName":"create_organization",
            "name": name,   
            "users": users, 
        })
    return validate_response(payload, headers=headers)

def check_connection(conn):
    # """CHECKS FOR A VALID CONNECTION"""
    if (len(conn.split(":")) == 2) :
        return {  "user-secret" :conn.split(":")[0],  "pipeline":  conn.split(":")[1]}
    else:
        return False

def create_headers(user , pipeline = ''):
    return {  "user-secret" :user,  "pipeline":pipeline}

def validate_response(payload, headers):
    # """IF 'message', THEN ERROR"""
    response = requests.post(url ,data= payload,headers= headers)
    response = json.loads(response.text)
    if ('message' in response):
        return  (response['message'])
    else :
        return response

def validate_response_download(payload, headers):
    # """IF 'message', THEN ERROR"""
    response = requests.post(url ,data= payload,headers= headers)
    return response

def validate_response_upload(func, file,table ,  headers):
    files = {'file': open(file,'rb')}
    payload ={ 'table_name' : table, 'file_path':int(time.time())  }
    # payload ={ 'table' : table }
    # print(payload)
    response = requests.post(url_upload,data =payload, files=files,headers= headers)
    response = json.loads(response.text)
    if ('message' in response):
        return  (response['message'])
    else :
        return response
   
 