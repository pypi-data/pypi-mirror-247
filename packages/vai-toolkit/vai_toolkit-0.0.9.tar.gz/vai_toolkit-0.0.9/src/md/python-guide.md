# Python Guide

This is our Python Guide for ML development. See Tables. Below

<br>
Table 1. vai_toolkit.client()

| Method                                                                 | Description                                                       |
| ---------------------------------------------------------------------- | ----------------------------------------------------------------- |
| [client.create_organization()](#vai_toolkit.client.create_organization)| This method is used to create organization for user.              |
| [client.update_name()](#vai_toolkit.client.update_name)                | This method is used to update user's first name and last name.    |
| [client.update_password()](#vai_toolkit.client.update_password)        | This method is used to update user password.                      |

<br>
Table 2. vai_toolkit.pipeline()

| Method                                                           | Description                                                                          |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [pipeline.create()](#vai_toolkit.pipeline.create)                | This method is used to create pipeline of provided user.                             |
| [pipeline.create_alert()](#vai_toolkit.pipeline.create_alert)    | This method is used to create alert for given pipeline of user.                      |
| [pipeline.create_table()](#vai_toolkit.pipeline.create_table)                | This method is used to create table for given pipeline of user.                             |
| [pipeline.delete_pipeline()](#vai_toolkit.pipeline.delete_pipeline)                | This method is used to delete pipeline when there is no dataset in pipeline.                             |
| [pipeline.delete_table()](#vai_toolkit.pipeline.delete_table)                | This method is used to delete table for given pipeline of user.                          |
| [pipeline.get_table()](#vai_toolkit.pipeline.get_table)      | This method is used to get tables of given pipeline of user.            |
| [pipeline.list_alerts()](#vai_toolkit.pipeline.list_alerts)      | This method is used to get the list of alerts for given pipeline of user.            |
| [pipeline.set_default_table()](#vai_toolkit.pipeline.set_default_table)    | This method is used to set default table for given pipeline of user.                    |
| [pipeline.update_table()](#vai_toolkit.pipeline.update_table)    | This method is used to update table name for given pipeline of user.                         |

<br>

<br>
Table 3. vai_toolkit.data()

| Method                                                    | Description                                                                          |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [data.delete_data()](#vai_toolkit.data.delete_data)       | This method is used to delete dataset data for given range in pipeline of user.      |
| [data.download_csvs()](#vai_toolkit.data.download_csvs)   | This method is used to download dataset for given pipeline of user.                  |
| [data.list_labels()](#vai_toolkit.data.list_labels)       | This method is used to get labels for given pipeline of user.                        |
| [data.set_labels()](#vai_toolkit.data.set_labels)         | This method is used to set labels for given pipeline of user.                        |
| [data.set_relations()](#vai_toolkit.data.set_relations)         | This method is used to set relations between tables of given pipeline of user.                 |
| [data.upload_csv()](#vai_toolkit.data.upload_csv)         | This method is used to upload csv for given pipeline of user                         |
| [data.upload_data()](#vai_toolkit.data.upload_data)       | This method is used to upload data for given pipeline of user.                       |

<br>

<br>
Table 4. vai_toolkit.model()

| Method                                                               | Description                                                                                                                                 |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| [model.explain()](#vai_toolkit.model.explain)                          | This method is used to get explanability values of specific record for given pipeline of user with options "NEXT_SERIES" or "MIXED" or "NEXT_LINK", if "NEXT_SERIES" then get explanability values of specific record with timeseries on for given pipeline of user and if "MIXED" then get explanability values of specific record with timeseries off for given pipeline of user.                                                                                     |
| [model.history()](#vai_toolkit.model.history)                          | This method is used to get history of given model.                                                                                     |
| [model.predict()](#vai_toolkit.model.predict)                          | This method is used to get prediction of table count with different model two options available  "NEXT_SERIES" and "NEXT_LINK".                                                                                       |
| [model.train()](#vai_toolkit.model.train)                            | This method is used to train model with options "NEXT_SERIES", "MIXED" and "NEXT_LINK", if "NEXT_SERIES" then model will be trained with timeseries on for given pipeline of user and if "MIXED" then model will be trained with timeseries off for given pipeline of user.                                                                                                                                              |
| [model.delete()](#vai_toolkit.model.delete)                          | This method is used to delete given model.                                                                                     |
| [model.retrain()](#vai_toolkit.model.retrain)                          | This method is used to retrain given model.                                                                                     |

<br>

::: vai_toolkit.client
    handler: python
    options:
      members:
      show_root_heading: true
      show_source: false

<br>

<br>

::: vai_toolkit.pipeline
    handler: python
    options:
      members:
      show_root_heading: true
      show_source: false

<br>

::: vai_toolkit.data
    handler: python
    options:
      members:
      show_root_heading: true
      show_source: false

<br>

::: vai_toolkit.model
    handler: python
    options:
      members:
      show_root_heading: true
      show_source: false

<br>

<script src="./script.js"></script>
