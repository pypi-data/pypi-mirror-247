# TODO: make predict_time and predict_link like "func", "data"

from vai_toolkit.client import *
import json

def train(user_secret, pipeline_key, title,  from_date , to_date, settings, option,table_name='') -> object:
    """This method is used to train model with options "NEXT_SERIES", "MIXED" and "NEXT_LINK", if "NEXT_SERIES" then model will be trained with timeseries on for given pipeline of user and if "MIXED" then model will be trained with timeseries off for given pipeline of user.  
    
    args:

        user_secret {string}: It is the user secret key.
        pipeline_key {string}: It is the pipeline key.
        title {string}: It is the name of model you want to give
        from_date {string}: It is the date of dataset in pipeline from which model will create in 'MM-DD-YYYY' format, passed if the option is "NEXT_SERIES" and "MIXED" only.
        to_date {string}: It is the date of dataset in pipeline to which model will create in 'MM_DD_YYYY' format, passed if the option is "NEXT_SERIES" and "MIXED" only.
        settings {object}: It is a settings object passed if the option is "NEXT_LINK" only, object with required fields - `dates`, `trainNodeType`, `dummyNodeType`, `seedNodeType` and in `dates` field, add keys as `column_names` with its object values, for Ex. see below example of "NEXT_LINK" option.
        option {string}: It could be only "NEXT_SERIES", "MIXED" and "NEXT_LINK".
        table_name {string}: It is the name of table of which data needs to consider while creating model.

    returns: 

        type: Response message.
    
    Example:

        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import model

        user_secret = 'USER_SECRET_KEY'
        pipeline_key = 'PIPELINE_KEY'
        title = 'MODEL_TITLE'
        from_date = '01/01/2022'
        to_date = '05/30/2023'
        option='NEXT_SERIES' 
        table_name='Table 1'

        res= model.train( user_secret,pipeline_key,title, from_date,to_date, None, option , table_name =table_name)
        print(res)



        # train mixed model

        from vai_toolkit import model

        user_secret = 'USER_SECRET_KEY'
        pipeline_key = 'PIPELINE_KEY'
        title = 'MODEL_TITLE'
        from_date = '08/31/2023'
        to_date = '09/11/2023'
        option='MIXED' 
        table_name='Table 1'


        res= model.train( user_secret,pipeline_key,title, from_date,to_date, None,option , table_name =table_name)
        print(res)




        from vai_toolkit import model

        user_secret = 'USER_SECRET_KEY'
        pipeline_key = 'PIPELINE_KEY'
        title = 'MODEL_TITLE'

        option  = 'NEXT_LINK'
        settings  = {
            "dates": {
                "dim_item": {
                    "from": "01-01-2023",
                    "to": "12-31-2023",
                    "allDate": False
                },
                "check": {
                    "from": "01-01-2023",
                    "to": "12-31-2023",
                    "allDate": False 
                },
                "check_item": {
                    "from": "01-01-2023",
                    "to": "12-31-2023",
                    "allDate": False
                }
            },
            "trainNodeType": "check",
            "dummyNodeType": "check",
            "seedNodeType": "dim_item"
        }

        res= model.train( user_secret,pipeline_key,title,None,None,settings,option)
        print(res)
        </span>
        </code></pre>


    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
            "status": "In progress", 
            "model Id": "Model Id", 
            "apiKey": "Model api key."
        }</span>
        </code></pre>

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
            "status": "In progress", 
            "model Id": "Model Id", 
            "apiKey": "Model api key."
        }</span>
        </code></pre>

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
            "status": "In progress", 
            "model Id": "Model Id", 
            "apiKey": "Model api key."
        }</span>
        </code></pre>
    
    """

    if(option == "NEXT_SERIES" or option ==  "MIXED" or option == 'NEXT_LINK'):
        headers =create_headers(user_secret, pipeline= pipeline_key)
        payload= {}
        if(option =="NEXT_SERIES" or option ==  "MIXED" ):         
            if table_name:
                payload = json.dumps({ 
                        "functionName":( 'train_timeseries' if option == "NEXT_SERIES" else  ("train_mixed" if option =='MIXED' else 'next_link' )),
                        "title": title,
                        "fromDate": from_date,
                        "toDate": to_date,
                        "tableName":table_name
                    })
            else:
                return { "message" : "Table name is required." }
        else: 
            payload = json.dumps({ 
                "functionName":   'next_link',
                "title" : title,
                "settings": settings
            })
        return validate_response(payload, headers)
    else:
        return {"message":"Only NEXT_SERIES, MIXED and 'NEXT_LINK' as options are allowed in option."}

def predict(user_secret, pipeline_key, model_key, from_date, to_date, config, option) -> object:
    """This method is used to get prediction of table count with different model two options available  "NEXT_SERIES" and "NEXT_LINK".

    args:

        user_secret {string}: It is the user secret key.
        pipeline_key {string}: It is the pipeline key.
        model_key {string}: It is model key.
        from_date {string}: It is the date of dataset in pipeline from which model will create in 'MM-DD-YYYY' format, passed if the option is "NEXT_SERIES"  only.
        to_date {string}: It is the date of dataset in pipeline to which model will create in 'MM_DD_YYYY' format, passed if the option is "NEXT_SERIES" only.
        config {object}: It is the config object, passed if the option is "NEXT_LINK" only.
        option {string}: It could be only "NEXT_SERIES" or "NEXT_LINK".

    returns: 

        type: Response message.
    
    Example:

        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import model

        user_secret='USER_SECRET_KEY'
        pipeline_key = 'PIPELINE_KEY'
        model_key = 'MODEL_KEY' 

        from_date = '03/01/2023'
        to_date = '05/31/2023'
        option = 'NEXT_SERIES'
        
        res = model.predict(user_secret, pipeline_key, model_key ,from_date,to_date,None,option)
        print(res)



        from vai_toolkit import model

        user_secret = 'USER_SECRET_KEY'
        pipeline_key = 'PIPELINE_KEY'
        model_key ='MODEL_KEY'
        config ={
                "seedNodeNameCol" : 'ItemDescription',
                "prediction" : 10,
                "seedNodeNames" : ["1","2"],
                "refNodeDict" : {
                    "GuestCount" :0,
                    "CheckOpen" : "2023-09-08T05:14:05.283Z",
        }}
        option ='NEXT_LINK'

        res = model.predict(user_secret, pipeline_key, model_key, None,None, config, option)
        print(res)

        </span>
        </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
            {
                'data': {
                    'errorMessage': '', 
                    'traceback': '', 
                    'data': {
                        'y': [
                                {'date': '05-31-2023', 'counts': '[{"tableCount":281.7903747559,"time":11},{"tableCount":221.9609527588,"time":12},{"tableCount":136.3621520996,"time":13},{"tableCount":88.3298797607,"time":14}, {"tableCount":66.8720169067,"time":15},{"tableCount":53.803276062,"time":16},{"tableCount":84.1227493286,"time":17},{"tableCount":159.0596923828,"time":18},{"tableCount":186.9671936035,"time":19},{"tableCount":188.2597351074,"time":20},{"tableCount":192.5038146973,"time":21}]'},
                                {'date': '06-01-2023', 'counts': '[{"tableCount":221.7015228271,"time":11},{"tableCount":249.4067230225,"time":12},{"tableCount":262.0877990723,"time":13},{"tableCount":227.6030883789,"time":14},{"tableCount":163.640625,"time":15},{"tableCount":81.578666687,"time":16},{"tableCount":35.5799293518,"time":17},{"tableCount":25.2485866547,"time":18},{"tableCount":16.2483539581,"time":19},{"tableCount":56.0276679993,"time":20},{"tableCount":127.5245361328,"time":21}]'},
                                {'date': '06-02-2023', 'counts': '[{"tableCount":151.8760070801,"time":11},{"tableCount":149.3125305176,"time":12},{"tableCount":136.9319000244,"time":13},{"tableCount":138.5372772217,"time":14},{"tableCount":149.87840271,"time":15},{"tableCount":159.7752838135,"time":16},{"tableCount":138.3939819336,"time":17},{"tableCount":101.8885879517,"time":18},{"tableCount":51.3734474182,"time":19},{"tableCount":26.7129077911,"time":20},{"tableCount":25.0917453766,"time":21}]'}, 
                                {'date': '06-03-2023', 'counts': '[{"tableCount":15.0687656403,"time":11},{"tableCount":40.74168396,"time":12},{"tableCount":89.7492446899,"time":13},{"tableCount":101.6272888184,"time":14},{"tableCount":98.6197280884,"time":15},{"tableCount":94.0878372192,"time":16},{"tableCount":106.0318145752,"time":17},{"tableCount":128.7826690674,"time":18},{"tableCount":150.5857696533,"time":19},{"tableCount":137.3954925537,"time":20},{"tableCount":107.9107666016,"time":21}]'},
                                {'date': '06-04-2023', 'counts': '[{"tableCount":69.9748687744,"time":11},{"tableCount":48.4622573853,"time":12},{"tableCount":38.2721862793,"time":13},{"tableCount":23.1030216217,"time":14},{"tableCount":40.9192276001,"time":15},{"tableCount":80.6420669556,"time":16},{"tableCount":88.2661819458,"time":17},{"tableCount":88.1396331787,"time":18},{"tableCount":92.166053772,"time":19},{"tableCount":116.6257400513,"time":20},{"tableCount":148.4887084961,"time":21}]'}, 
                                {'date': '06-05-2023', 'counts': '[{"tableCount":169.0198364258,"time":11},{"tableCount":147.4364776611,"time":12},{"tableCount":108.4352493286,"time":13},{"tableCount":58.7132301331,"time":14},{"tableCount":31.183631897,"time":15},{"tableCount":28.5562381744,"time":16},{"tableCount":17.1293258667,"time":17},{"tableCount":44.2518920898,"time":18},{"tableCount":96.2329483032,"time":19},{"tableCount":95.2348632812,"time":20},{"tableCount":85.2216186523,"time":21}]'}, 
                                {'date': '06-06-2023', 'counts': '[{"tableCount":89.2415390015,"time":11},{"tableCount":117.0859832764,"time":12},{"tableCount":144.4945983887,"time":13},{"tableCount":158.9694213867,"time":14},{"tableCount":136.0721588135,"time":15},{"tableCount":91.8300094604,"time":16},{"tableCount":37.7490653992,"time":17},{"tableCount":20.4870605469,"time":18},{"tableCount":29.0067577362,"time":19},{"tableCount":17.4881305695,"time":20},{"tableCount":52.84141922,"time":21}]'}
                            ], 
                        'x': '', 
                        'note': 'predicting without explanation'
                }
            }
        }
        </span>
        </code></pre>
    """
    
    if(option == "NEXT_SERIES"  or option == 'NEXT_LINK'):
        headers =create_headers(user_secret,pipeline= pipeline_key)
        payload= {}
        if(option =="NEXT_SERIES"   ):
            payload = json.dumps({ 
                "functionName":  "predict_time",
                "model": model_key,
                "fromDate" : from_date,
                "toDate" : to_date,
            })
        else: 
            payload = json.dumps({ 
                "functionName":   'predict_next_link',
                "model": model_key,
                "config":config
            })
        return validate_response( payload,headers)
    else:
        return {"message":"Only NEXT_SERIES  as options is allowed in option."}


def explain(user_secret, pipeline_key, model_key, datasetData= None, dataset= None, from_date= None , to_date= None, config = None , option="") -> object:
    """This method is used to get explanability values of specific record for given pipeline of user with two options "NEXT_SERIES" or "MIXED", if "NEXT_SERIES" then get explanability values of specific record with timeseries on for given pipeline of user and if "MIXED" then get explanability values of specific record with timeseries off for given pipeline of user.

    args:

        user_secret {string}: It is the user secret key.
        pipeline_key {string}: It is the pipeline key.
        model_key {string}: It is model key.
    
    Keyword Arguments:

        datasetData {string}: It is dataset data value passed if the option is "MIXED" only.
        dataset {string}: It is dataset value passed if the option is "MIXED" only.
        from_date {string}: It is from date string passed if the option is "NEXT_SERIES" only.
        to_date {string}: It is to date string passed if the option is "NEXT_SERIES" only.
        config {object}: It is the config object if the option is "NEXT_LINK" only..
        option {string}: It could be only "NEXT_SERIES" or "MIXED".

    returns: 

        type: Response message.
    
    Example:
        
        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import model

        user_secret = 'USER_SECRET_KEY'
        pipeline_key = 'PIPELINE_KEY'
        model_key ='MODEL_KEY'

        from_date = '03/01/2023'
        to_date = '05/31/2023'
        option='NEXT_SERIES'

        res = model.explain(user_secret, pipeline_key, model_key ,from_date=from_date,to_date=to_date,option=option)
        print(res)




        from vai_toolkit import model

        user_secret = 'USER_SECRET_KEY'
        pipeline_key = 'PIPELINE_KEY'
        model_key ='MODEL_KEY'

        datasetData ={
            "hours-per-week": 35,
            "age" : 40,
            "loan-approved":0,
            "capital-gain": 0,
            "capital-loss": 0,
            "education": "HS-grad",
            "education-num": 9,
            "marital-status": "Never-married",
            "native-country": "United-States",
            "occupation": "Transport-moving",
            "race": "Non-white",
            "relationship": "Not-in-family",
            "sex": "Male",
            "workclass": "Private"
        }
        dataset ="08-31-2023"

        res = model.explain(user_secret, pipeline_key,model_key, datasetData=datasetData,dataset=dataset, option="MIXED" )
        print(res)


        
        from vai_toolkit import model

        user_secret = 'USER_SECRET_KEY'
        pipeline_key = 'PIPELINE_KEY'
        model_key ='MODEL_KEY'
        config ={
                "seedNodeNameCol" : 'ItemDescription',
                "prediction" : 10,
                "seedNodeNames" : ["1","2"],
                "refNodeDict" : {
                    "GuestCount" :0,
                    "CheckOpen" : "2023-09-08T05:14:05.283Z",
        }}
        option ='NEXT_LINK'

        res = model.explain(user_secret, pipeline_key, model_key, config=config, option=option)
        print(res)
        </span>
        </code></pre>


    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">{
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
        }</span>
        </code></pre>


        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text"> {
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
        }</span>
        </code></pre>
    """

    if(option == "NEXT_SERIES" or option ==  "MIXED" or option == 'NEXT_LINK' ) :
            headers =create_headers(user_secret, pipeline= pipeline_key)    
            payload ={ }
            if(option == "NEXT_SERIES"):
                if(from_date and to_date):
                    payload=json.dumps({ 
                        "functionName" :  "explain_timeseries",
                        "model": model_key,
                        "fromDate":from_date,
                        "toDate": to_date
                    }) 
                else:
                   return {"message":"Please provide fromdate and todate for next series option."}
            if( option ==  "MIXED"):
                if(datasetData and dataset):
                    payload=json.dumps({ 
                        "functionName":  "explain",
                        "datasetData": datasetData,
                        "model": model_key,
                        "dataset": dataset,
                    })
                else:
                   return {"message":"Please provide dataset data and dataset for mixed option."}
            if(option == 'NEXT_LINK'):
                payload = json.dumps({ 
                    "functionName":  'explain_link',
                    "model": model_key,
                    "config":config
                })
            return validate_response( payload,headers)
    else:
        return {"message":"Only NEXT_SERIES and MIXED as options are allowed in option."}
    


def history(user_secret, pipeline_key, model_key, limit =5 )  -> object:
    """This method is used to get history of given model.

    args:

       user_secret {string}: It is the user secret key.
       pipeline_key {string}: It is the pipeline key.
       model_key {string}: It is the model key.
       limit {number}: It is limit used to specify a particular constraint for retrieving history data.


    returns: 

        type:  Get response containing input and output.
    
    Example:
        
        <pre class="content-block ml-20"><div class="copy-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
        </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import model

        user_secret = 'USER_SECRET_KEY'
        pipeline_key = 'PIPELINE_KEY'
        model_key = 'MODEL_KEY'
        limit = 5

        res= model.history( user_secret, pipeline_key, model_key, limit)
        print(res)
        </span>
        </code></pre>


    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">[
            {
                "id": "65260a39bb6b899f4d789222",
                "input": {
                    "fromDate": "12/21/2022",
                    "toDate": "12/31/2022"
                },
                "output": {
                    "data": {
                        "errorMessage": "",
                        "traceback": "",
                        "data": {
                            "y": [
                                {
                                  "date": "01-01-2023",
                                  "counts": "[{\"tableCount\":8.1729021072,\"time\":11},{\"tableCount\":9.2272834778,\"time\":12},{\"tableCount\":8.7410840988,\"time\":13},{\"tableCount\":7.2610864639,\"time\":14},{\"tableCount\":4.7990121841,\"time\":15},{\"tableCount\":4.9796061516,\"time\":16},{\"tableCount\":5.1875333786,\"time\":17},{\"tableCount\":6.0545682907,\"time\":18},{\"tableCount\":6.2240757942,\"time\":19},{\"tableCount\":6.6397485733,\"time\":20},{\"tableCount\":6.5043768883,\"time\":21}]"
                                },
                                {
                                  "date": "01-02-2023",
                                  "counts": "[{\"tableCount\":5.9584774971,\"time\":11},{\"tableCount\":4.71900177,\"time\":12},{\"tableCount\":5.23458004,\"time\":13},{\"tableCount\":5.9814653397,\"time\":14},{\"tableCount\":5.5183796883,\"time\":15},{\"tableCount\":6.3703117371,\"time\":16},{\"tableCount\":3.9970772266,\"time\":17},{\"tableCount\":1.6930608749,\"time\":18},{\"tableCount\":2.1605021954,\"time\":19},{\"tableCount\":2.2661693096,\"time\":20},{\"tableCount\":4.5692014694,\"time\":21}]"
                                },
                                {
                                  "date": "01-03-2023",
                                  "counts": "[{\"tableCount\":4.8561573029,\"time\":11},{\"tableCount\":5.6609015465,\"time\":12},{\"tableCount\":3.6423728466,\"time\":13},{\"tableCount\":4.340628624,\"time\":14},{\"tableCount\":7.3471589088,\"time\":15},{\"tableCount\":8.417137146,\"time\":16},{\"tableCount\":11.6935253143,\"time\":17},{\"tableCount\":13.3711690903,\"time\":18},{\"tableCount\":12.0397434235,\"time\":19},{\"tableCount\":9.6431388855,\"time\":20},{\"tableCount\":10.8736925125,\"time\":21}]"
                                },
                                {
                                  "date": "01-04-2023",
                                  "counts": "[{\"tableCount\":9.326757431,\"time\":11},{\"tableCount\":9.4327068329,\"time\":12},{\"tableCount\":8.0079860687,\"time\":13},{\"tableCount\":5.2251749039,\"time\":14},{\"tableCount\":2.5511522293,\"time\":15},{\"tableCount\":2.8028771877,\"time\":16},{\"tableCount\":2.1789927483,\"time\":17},{\"tableCount\":3.3140306473,\"time\":18},{\"tableCount\":2.8704621792,\"time\":19},{\"tableCount\":3.9721398354,\"time\":20},{\"tableCount\":7.6661634445,\"time\":21}]"
                                },
                                {
                                  "date": "01-05-2023",
                                  "counts": "[{\"tableCount\":7.1075911522,\"time\":11},{\"tableCount\":5.5151014328,\"time\":12},{\"tableCount\":8.0471925735,\"time\":13},{\"tableCount\":6.7182812691,\"time\":14},{\"tableCount\":8.4082269669,\"time\":15},{\"tableCount\":9.8997507095,\"time\":16},{\"tableCount\":7.8638906479,\"time\":17},{\"tableCount\":9.3877916336,\"time\":18},{\"tableCount\":10.8658905029,\"time\":19},{\"tableCount\":10.8907938004,\"time\":20},{\"tableCount\":8.6171550751,\"time\":21}]"
                                },
                                {
                                  "date": "01-06-2023",
                                  "counts": "[{\"tableCount\":10.2738752365,\"time\":11},{\"tableCount\":11.7885751724,\"time\":12},{\"tableCount\":14.5384082794,\"time\":13},{\"tableCount\":13.7233953476,\"time\":14},{\"tableCount\":10.7814865112,\"time\":15},{\"tableCount\":10.6480283737,\"time\":16},{\"tableCount\":11.9552650452,\"time\":17},{\"tableCount\":12.1137609482,\"time\":18},{\"tableCount\":9.6347846985,\"time\":19},{\"tableCount\":9.3301410675,\"time\":20},{\"tableCount\":8.0276508331,\"time\":21}]"
                                },
                                {
                                  "date": "01-07-2023",
                                  "counts": "[{\"tableCount\":9.2904233932,\"time\":11},{\"tableCount\":10.0985774994,\"time\":12},{\"tableCount\":8.670334816,\"time\":13},{\"tableCount\":9.018081665,\"time\":14},{\"tableCount\":10.2240543365,\"time\":15},{\"tableCount\":12.6987085342,\"time\":16},{\"tableCount\":10.0400686264,\"time\":17},{\"tableCount\":6.4473996162,\"time\":18},{\"tableCount\":8.7904291153,\"time\":19},{\"tableCount\":9.4310073853,\"time\":20},{\"tableCount\":9.7929801941,\"time\":21}]"
                                }
                            ],
                         "x": "",
                        "note": "predicting without explanation"
                    }
                }
             }
        },
        {
            "id": "65260a39bb6b899f4d789223",
            "input": {
                "fromDate": "12/21/2022",
                "toDate": "12/31/2022"
            },
            "output": {
                "data": {
                    "errorMessage": "",
                    "traceback": "",
                    "data": {
                        "y": [
                            {
                                "date": "01-01-2023",
                                "counts": "[{\"tableCount\":8.1729021072,\"time\":11},{\"tableCount\":9.2272834778,\"time\":12},{\"tableCount\":8.7410840988,\"time\":13},{\"tableCount\":7.2610864639,\"time\":14},{\"tableCount\":4.7990121841,\"time\":15},{\"tableCount\":4.9796061516,\"time\":16},{\"tableCount\":5.1875333786,\"time\":17},{\"tableCount\":6.0545682907,\"time\":18},{\"tableCount\":6.2240757942,\"time\":19},{\"tableCount\":6.6397485733,\"time\":20},{\"tableCount\":6.5043768883,\"time\":21}]"
                            },
                            {
                                "date": "01-02-2023",
                                "counts": "[{\"tableCount\":5.9584774971,\"time\":11},{\"tableCount\":4.71900177,\"time\":12},{\"tableCount\":5.23458004,\"time\":13},{\"tableCount\":5.9814653397,\"time\":14},{\"tableCount\":5.5183796883,\"time\":15},{\"tableCount\":6.3703117371,\"time\":16},{\"tableCount\":3.9970772266,\"time\":17},{\"tableCount\":1.6930608749,\"time\":18},{\"tableCount\":2.1605021954,\"time\":19},{\"tableCount\":2.2661693096,\"time\":20},{\"tableCount\":4.5692014694,\"time\":21}]"
                            },
                            {
                                "date": "01-03-2023",
                                "counts": "[{\"tableCount\":4.8561573029,\"time\":11},{\"tableCount\":5.6609015465,\"time\":12},{\"tableCount\":3.6423728466,\"time\":13},{\"tableCount\":4.340628624,\"time\":14},{\"tableCount\":7.3471589088,\"time\":15},{\"tableCount\":8.417137146,\"time\":16},{\"tableCount\":11.6935253143,\"time\":17},{\"tableCount\":13.3711690903,\"time\":18},{\"tableCount\":12.0397434235,\"time\":19},{\"tableCount\":9.6431388855,\"time\":20},{\"tableCount\":10.8736925125,\"time\":21}]"
                            },
                            {
                                "date": "01-04-2023",
                                "counts": "[{\"tableCount\":9.326757431,\"time\":11},{\"tableCount\":9.4327068329,\"time\":12},{\"tableCount\":8.0079860687,\"time\":13},{\"tableCount\":5.2251749039,\"time\":14},{\"tableCount\":2.5511522293,\"time\":15},{\"tableCount\":2.8028771877,\"time\":16},{\"tableCount\":2.1789927483,\"time\":17},{\"tableCount\":3.3140306473,\"time\":18},{\"tableCount\":2.8704621792,\"time\":19},{\"tableCount\":3.9721398354,\"time\":20},{\"tableCount\":7.6661634445,\"time\":21}]"
                            },
                            {
                                "date": "01-05-2023",
                                "counts": "[{\"tableCount\":7.1075911522,\"time\":11},{\"tableCount\":5.5151014328,\"time\":12},{\"tableCount\":8.0471925735,\"time\":13},{\"tableCount\":6.7182812691,\"time\":14},{\"tableCount\":8.4082269669,\"time\":15},{\"tableCount\":9.8997507095,\"time\":16},{\"tableCount\":7.8638906479,\"time\":17},{\"tableCount\":9.3877916336,\"time\":18},{\"tableCount\":10.8658905029,\"time\":19},{\"tableCount\":10.8907938004,\"time\":20},{\"tableCount\":8.6171550751,\"time\":21}]"
                            },
                            {
                                "date": "01-06-2023",
                                "counts": "[{\"tableCount\":10.2738752365,\"time\":11},{\"tableCount\":11.7885751724,\"time\":12},{\"tableCount\":14.5384082794,\"time\":13},{\"tableCount\":13.7233953476,\"time\":14},{\"tableCount\":10.7814865112,\"time\":15},{\"tableCount\":10.6480283737,\"time\":16},{\"tableCount\":11.9552650452,\"time\":17},{\"tableCount\":12.1137609482,\"time\":18},{\"tableCount\":9.6347846985,\"time\":19},{\"tableCount\":9.3301410675,\"time\":20},{\"tableCount\":8.0276508331,\"time\":21}]"
                            },
                            {
                                "date": "01-07-2023",
                                "counts": "[{\"tableCount\":9.2904233932,\"time\":11},{\"tableCount\":10.0985774994,\"time\":12},{\"tableCount\":8.670334816,\"time\":13},{\"tableCount\":9.018081665,\"time\":14},{\"tableCount\":10.2240543365,\"time\":15},{\"tableCount\":12.6987085342,\"time\":16},{\"tableCount\":10.0400686264,\"time\":17},{\"tableCount\":6.4473996162,\"time\":18},{\"tableCount\":8.7904291153,\"time\":19},{\"tableCount\":9.4310073853,\"time\":20},{\"tableCount\":9.7929801941,\"time\":21}]"
                            }
                        ],
                        "x": "",
                        "note": "predicting without explanation"
                    }
                }
             }
          }               
        ]</span>
        </code></pre>
    """
    headers = create_headers(user_secret, pipeline = pipeline_key)
    payload = json.dumps({
        "functionName": "history",
        "limit" : limit,
        "model": model_key
    })
    return validate_response(payload, headers)

def delete(user_secret, pipeline_key, model_key)-> object:
    """This method is used to delete model of provided pipeline. 

    args:

            user_secret {string}: It is the user secret key.
            pipeline_key {string}: It is the pipeline key.
            model_key {string}: It is the model key.

    returns: 

            type:Success response message.
    Example:

            <pre class="content-block ml-20"><div class="copy-button">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
            <div class="copy-text"></div>
            </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import pipeline

            user_secret  =  'USER_SECRET_KEY'
            pipeline_key =  'PIPELINE_KEY'
            model_key = 'MODEL_KEY'

            res = model.delete(user_secret, pipeline_key ,model_key)
            print(res)
            </span>
            </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">Model deleted successfully.
            
        </span>
        </code></pre>"""
    headers =create_headers(user_secret, pipeline = pipeline_key)

    payload = json.dumps({
            "functionName": "delete_model",
        "model": model_key
        })

    return validate_response(payload,headers) 

def retrain(user_secret, pipeline_key, model_key)-> object:
    """This method is used to delete model of provided pipeline. 

    args:

            user_secret {string}: It is the user secret key.
            pipeline_key {string}: It is the pipeline key.
            model_key {string}: It is the model key.

    returns: 

            type: Success response message.
    Example:

            <pre class="content-block ml-20"><div class="copy-button">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
            <div class="copy-text"></div>
            </div><code class="hljs vbnet python-guide"><span id="text">from vai_toolkit import pipeline

            user_secret  =  'USER_SECRET_KEY'
            pipeline_key =  'PIPELINE_KEY'
            model_key = 'MODEL_KEY'

            res = model.retrain(user_secret, pipeline_key ,model_key)
            print(res)
            </span>
            </code></pre>

    Output:

        <pre class="content-block ml-20"><code class="hljs vbnet rest-guide"><span id="text">Model retrained successfully.
        </span>
        </code></pre>"""
    headers =create_headers(user_secret, pipeline = pipeline_key)

    payload = json.dumps({
        "functionName": "retrain_model",
        "model": model_key
        })

    return validate_response(payload,headers) 