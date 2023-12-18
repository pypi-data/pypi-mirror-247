# Dataset

| Method               | Description                                    |
| ------------------   | ---------------------------------------------- |
| [automation.bulk_pipelines(file)](#1bulk_pipelinesfile) | Use to insert bulk users, pipelines, locations and accesses in bulk |
| [automation.bulk_upload(file)](#2bulk_uploadfile) | Use to insert data in bulk |
| [automation.bulk_models(file)](#3bulk_modelsfile) | Use to insert model in bulk |
| [automation.bulk_accounts(file)](#4bulk_accountsfile) | Use to add access to accounts|

<br>

## 1.bulk_pipelines(file)

<pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
  <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">automation.bulk_pipelines(
        file_path
    )</span>
</code></pre>
    

Parameters

<pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
  <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">file_path: file path of file to pass</span>
</code></pre>

    


Below is the code for valid file
<br>
<pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "owner": "billing+6@ziosk.com",
    "organizations": {
        "Red Robins": {
            "pipelines": {
                "Red Robins 12": {
                    "locations": [
                        "RRGB0097",
                        "RRGB0102",
                        "RRGB0121",
                        "RRGB0194",
                        "RRGB0259",
                        "RRGB0318",
                        "RRGB0319",
                        "RRGB0593",
                        "RRGB0600",
                        "RRGB0612",
                        "RRGB0736"
                    ]
                }
            }
        }
    }
}</span>                               
</code></pre>

<br>
<br>

## 2.bulk_upload(file)

<pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
  <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">automation.bulk_upload(
    file_path
)</span>
</code></pre>


Parameters

<pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
  <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">file_path: file path of file to pass</span>
</code></pre>





Below is the code for valid file
<br>
<pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "owner": "billing+6@ziosk.com",
    "organizations": {
        "Red Robins": {
                "pipelines": {
                "Red Robins 12": {
                    "RRGB0121": [
                            "./0/01-01-2022.csv",
                            "./0/01-02-2022.csv",
                            "./0/01-03-2022.csv",
                            "./0/01-04-2022.csv",
                            "./0/01-05-2022.csv"
                    ],
                    "RRGB0097": [
                             "./097/01-01-2022.csv",
                             "./097/01-01-2023.csv",
                             "./097/01-02-2022.csv",
                             "./097/01-02-2023.csv",
                             "./097/01-03-2022.csv",
                             "./097/01-03-2023.csv",
                             "./097/01-04-2023.csv",
                             "./097/01-05-2022.csv"
                    ],
                    "RRGB0102": [
                            "./102/01-01-2022.csv",
                            "./102/01-01-2023.csv",
                            "./102/01-02-2022.csv",
                            "./102/01-02-2023.csv",
                            "./102/01-03-2022.csv",
                            "./102/01-03-2023.csv",
                            "./102/01-04-2023.csv"
                        
                    ]
                }
            }
        }
    }
}</span>
</code></pre>


                            

<br>
<br>

## 3.bulk_models(file)

<pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
  <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">automation.bulk_models(
    file_path
)</span>
</code></pre>




Parameters

<pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
  <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">file_path: file path of file to pass</span>
</code></pre>

    


Below is the code for valid file
<br>
<pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
  <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "owner": "billing+6@ziosk.com",
    "organizations": {
        "Red Robins": {
                "pipelines": {
                    "Red Robins 12": {
                        "RRGB0097": {
                                "models": {
                                    "Model 1": {
                                        "fromDate": "01-01-2022",
                                        "toDate": "01-01-2022"
                                    },
                                    "Model 2": {
                                        "fromDate": "01-01-2022",
                                        "toDate": "01-01-2022"
                                    }
                                },
                                "Custom analytics": {
                                    "Control Panel 1": {
                                        "Widget 1": {
                                                "fields": [
                                                "Total"
                                                ]
                                        },
                                        "Widget 2": {
                                                "fields": [
                                                "Total"
                                                ]
                                        }
                                    },
                                    "Control Panel 2": {
                                        "Widget 1": {
                                                "fields": [
                                                "Total"
                                                ]
                                        },
                                        "Widget 2": {
                                                "fields": [
                                                "Total"
                                                ]
                                        }
                                    }
                                }
                        }
                    }
                }
        }
    }
}</span>
</code></pre>

    
<br>
<br>

## 4.bulk_accounts(file)

<pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
  <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">automation.bulk_accounts(
    file_path
)</span>
</code></pre>


Parameters

<pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
  <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">file_path: file path of file to pass</span>
</code></pre>

    


Below is the code for valid file
<br>

<pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
  <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "owner": "billing+6@ziosk.com",
    "organizations": {
        "Red Robins": {
            "users" : {
                "ziok+1@gmail.com": "ADMIN",
                "rory+2@gmail.com": "DEVELOPER",
                "alan+3@gmail.com": "FINANCIAL"
            },
            "pipelines": {
                "Red Robins 12": {
                    "locations": {
                        "sfsdf" : {
                            "users" : {
                                "ziok+1@gmail.com": "ADMIN",
                                "rory+2@gmail.com": "DEVELOPER",
                                "alan+3@gmail.com": "FINANCIAL"
                            }
                        }
                    }
                }
            }
        }
    }
}</span>
</code></pre>

    
<script src="./script.js"></script>