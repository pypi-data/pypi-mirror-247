# QUICKSTART

VAI Toolkit is the API for interacting with the Virtuous AI cloud platform. 

<br>

<pre class="content-block"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">pip install -i https://test.pypi.org/simple/ vai-toolkit</span></code></pre>

<br>

<pre class="content-block"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">from vai_toolkit import (client, pipeline, data, model) </span></code></pre>

<br>


<h2>Common Commands</h2>

These following are the most common commands, to keep in your pocket.

<!-- 1. Connect to pipeline: <pre class="content-block"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">conn = client.login(email, password)</span></code></pre></code> -->

1. Upload data: <pre class="content-block"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">data.upload_data(user_secret, pipeline_key, data, date, time,  new_columns=False, duplicates=False, new_categories=False, table_name='')</span></code></pre></code>

2. Interact: <pre class="content-block"><div class="copy-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#c9c9c9" d="M15 1H4c-1.1 0-2 .9-2 2v13c0 .55.45 1 1 1s1-.45 1-1V4c0-.55.45-1 1-1h10c.55 0 1-.45 1-1s-.45-1-1-1zm.59 4.59l4.83 4.83c.37.37.58.88.58 1.41V21c0 1.1-.9 2-2 2H7.99C6.89 23 6 22.1 6 21l.01-14c0-1.1.89-2 1.99-2h6.17c.53 0 1.04.21 1.42.59zM15 12h4.5L14 6.5V11c0 .55.45 1 1 1z"/></svg>
    <div class="copy-text"></div>
  </div><code class="hljs vbnet"><span id="text">model.predict(user_secret, pipeline_key, model_key, from_date, to_date, config, option)</span></code></pre></code>

<br>

<h2>Definitions</h2>

Understanding the terminology below that will make development much easier.

1. <b> Owner</b>: the billing account which creates the initial account

2. <b> Organization:</b> an entity with resources that are isolated from other organizations

3. <b> Pipeline:</b> a project with all of the pooled resources need to perform a business objective</span>
  <pre><b &nbsp>   - Location:</b> Isolate data groups with their own permissions that widgets bid to and models span.</span></pre>

4. <b> Model:</b> a model trained on data to perform on or numerous tasks (e.g. classification, prediction, or other inference)</span>

5. <b> Widget:</b> Objects used to interact with our platform in numerous ways to easily integrate with your application needs.</span >

<br>

(See the next section for an introduction)

<script src="./script.js"></script>
