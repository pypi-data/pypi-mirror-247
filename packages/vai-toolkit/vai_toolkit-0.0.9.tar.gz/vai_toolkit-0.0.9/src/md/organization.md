
# 3. Bulk Actions

<b><u>Purpose:</u></b> This is how easy it is to get started. By the end of this tutorial, you should be comfortable creating in bulk. **<b>Note:</b> please refer to the data overview if the following plot is not familiar, its a VERY quick read (< two minute read) 


 As a refresher,

 * there can be a one model to many type of relationship. 
 * There is one location to one widget
 * but you can have one model for multiple locations. 
 <br>


 <br>

![overview](./img/overview.png)

<br>
Fig. 1. The Pipeline Heirarchy with Its Multiple Layers of Security.
<br>
<br>

To create pipelines and bulk, first you create a pipelines configuration file. 

<br>

## 3.1. Bulk Create Pipelines

To start, first you need to ask a series of questions. As you answer them, note the answers in the configuration file. See below,

<b>example-pipelines.json</b>

<pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg><div class="copy-text"></div></div><code class="hljs vbnet"><span id="text">{
    "owner": "billing@example-domain.com",
    "organizations": {
        "Example Org": {
            "pipelines": {
                "Example Pipeline": {
                    "locations": [
                        "Example Location 1"</span></code></pre>
<br>

The following details how to fill in the information.

<br>

1. Were require at least one user to own the account. So the first question is, who is paying? That will be the owner.
    <pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
    </div><code class="hljs vbnet"><span class="text">“owner”: “billing@example-domain.com”</span></code></pre>
2. Next, the account owner can create one or more organizations to host pipelines. Currently, organizations are isolated entities. <br
    <pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
    </div><code class="hljs vbnet"><span class="text">“organizations”: {”Example Org 1": ...}</span></code></pre>
3. Organizations now need items with objects that users can interact with. You set up this environment using a pipeline.
    <pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg><div class="copy-text"></div></div><code class="hljs vbnet"><span id="text">“pipelines”: {”Example Pipeline 1": ...}</span></code></pre>
4. Often you may have a dataset that many would benefit from, but you may have restrictions on which data they can view. (e.g., various banks wherein staff need not access other location data.) You can optionally achieve this restricting by inserting the following.
    <pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg><div class="copy-text"></div></div><code class="hljs vbnet"><span id="text">locations: ["example Location 1", ...]</span></code></pre>
5. You can now create the pipelines by running the following script,
    <br>
    <pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg><div class="copy-text"></div></div><code class="hljs vbnet"><span id="text">organization.bulk_add("pipeline.json”)</span></code></pre>
    <br>

Next, you need to add data; see the Pipelines Section.

<br>

## 3.2. Bulk Add Data

After creating a pipeline, you must add the data required to interact. 

1. You can do that by reusing the previous file to iterate over for adding the data. 
    <b>data.json</b>
    <pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg><div class="copy-text"></div></div><code class="hljs vbnet"><span id="text">{
    "owner": "billing@example-domain.com",
    "organizations": {
        "Example Org": {
            "pipelines": {
                "Example Pipeline 1": {
                    "Example Location 1": ["data/location1/01-01-2023.csv", data/...</span>
    </code></pre>
2. You can now add data to the pipelines by running the following command.
    <br>
    <pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg><div class="copy-text"></div></div><code class="hljs vbnet"><span id="text">organization.bulk_data(data.json”)</span></code></pre>
    <br>

## 3.3. Bulk Create Widgets/Models
Next, we must create objects for the end users to interact with. Knowing your user’s needs unleashes a lot of opportunities. For example, the product could be widgets in the form of reports or events, such as table count next item predictions.

1. First, you have to think about who the machine learning product users are.  Some examples include the following: <b>MGMT:</b> want to track a few heuristics to improve operations.  <b>Staff:</b> want to make quicker, more accurate decisions on the floor. 

    Thus, you might determine that you will create two objects to interact with. Eg. for the managers you will run on a calendar event invoked by a model that aggregates a certain ML models heuristics statistics. Whereas for the staff you will invoke a widget for on device that helps provide recommendations every time a button is clicked. <br>
    <br>
    <b>model.json</b>
    <pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "owner": "billing@example-domain.com",
    "organizations": {
        "Example Org": {
            "pipelines": {
                "Example Pipeline 1": {
                    "Example Location 1": {
                        "models": {
                            "Example Model 1": {
                                "fromDate": "01-01-2023",
                                "toDate": "06-01-2023"
                            }
                        },</span>
    </code></pre>

2. Where the model.json excepts the same parameters as the RESTAPI and the UX, like below,

    <b>model.json(line 8)</b>

    <pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
    </div><code class="hljs vbnet"><span id="text">"models": {
            "next-item": {
                params: {
                    "timeseries": True,
                    "x": {},
                    "y": {},
                    "pipeline": "2890379nvjs"
                    "user_secret": "lkjho823hikuwn"
                }
            }
        }</span>
        </code></pre>
        <pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg><div class="copy-text"></div></div><code class="hljs vbnet"><span id="text">organization.bulk_data(data.json”)</span></code></pre>

3. After some time for training, say 15 minutes, you can add widgets to those models.
<br>

    <b>widget.json(line 8)</b>

    <pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
    </div><code class="hljs vbnet"><span id="text">"widgets": {
            "Last Week Staffing": {
                params: {
                    "timeseries": True,
                    "x": {},
                    "y": {},
                    "pipeline": "2890379nvjs"
                    "user_secret": "lkjho823hikuwn"
                }
            }
        }</span>
    </code></pre>

4. Calendar events can be scheduled using standard daemons (like cronjobs), which can call API at a particular time to send emails.
    <pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
        <div class="copy-text"></div>
    </div><code class="hljs vbnet"><span id="text">crontab -e
    [RESTAPI CALL GOES HERE]</span>
    </code></pre>

<br>
<br>

## 3.4. Bulk Adding Org. User

1. Lastly, you will need to create users to access the objects. 


<pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">{
    "owner": "billing@example-domain.com",
    "organizations": {
        "Example Org": {
            "users": {
                "billing@example-domain.com": "FINANCIAL",
                "dev@example-domain.com": "DEVELOPER"
            },
            "pipelines": {
                "Example Pipeline 1": {
                    "locations": {
                        "Example Location 1": {
                            "users": {
                                "billing@example-domain.com": "VIEWER",</span>
</code></pre>

Save that output. Now you have everything you need to create cronjob or trigger events in your platform using our corresponding API.





<script src="./script.js"></script>
