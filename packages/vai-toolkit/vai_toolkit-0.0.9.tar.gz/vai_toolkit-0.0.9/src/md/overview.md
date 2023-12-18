# 1. Overview

Virtuous AI uses data "pipelines" - an ML term – as abstractions to have high security and flexibility at scale, see below.


<br>

![overview](./img/overview.png)

<br>
<b>Fig. 1.</b> The Pipeline Heirarchy with Its Multiple Layers of Security.
<br>

As can be seen, there can be a one model to many type of relationship. There is one location to one widget, but you can have one model for multiple locations.

1. (optional) First an account <b>OWNER</b> can create multiple entities accounts (called <b>ORGANIZATION</b>) that act in isolation. 

2. Each personal/organizational account can create multiple <b>PIPELINE</b>.” Pipelines automate your end-to-end data processing. 

3. (optional) Pipelines contain data that can be partitioned into groups called <b>LOCATIONS</b> for increased security measures.

4. <b>MODEL</b> objects can be accessed via REST API after training on your data, but the real magic happens with the <b>WIDGETS</b> 

The owner of an paid account is the account with the "FINANCIAL" role.


<br>

<script src="./script.js"></script>










