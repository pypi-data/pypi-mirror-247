# Pipelines

##  Step 1: Create Pipeline

First step is to create a pipeline. You should do this through the UX or using our API.

<br>


##  Step 2: Add Data

After creating a pipeline, you need to add data that are required to interact with. The file naming convention is the following

<b><u>Filename:</u></b>

>
- location_MM:DD:YY.csv: files stored by the "date" + “.csv”

<b><u>Timestamps:</u></b>

>
- “HH:MM: SS”: column for the time stamps else. It will default to the current time.

You upload csv data using the following command. (See our API for more detail, we have REST as well)

<pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">account.add_csv("01-01-01.csv")</span>
</code></pre>

<br>

## Step 3:  Train Models and Add Widgets

Next, we must create objects for the end users to interact with. 

<pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">pipeline.train_model(conn, **params)</span>
</code></pre>

An example of possible training parameters might be the following (look at the API for more information)

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
    }</span>
</code></pre>


After some time for training, say 15 minutes, you can add widgets to those models.
<br>

<pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
      <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">pipeline.add_widdet(conn, **params)</span>
</code></pre>

<br>

## Step 4:  Monitor Events

Lastly, we can create events to track events such as data drift. (This may indicate that there is a problem that needs to be addressed). 

<pre class="content-block"><div class="copy-button" onclick="copyContentToClipboard(this)">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">pipeline.add_alert(conn, **params)</span>
</code></pre>

This will be triggered based on whatever your metrics you defined.

<br>

<script src="./script.js"></script>