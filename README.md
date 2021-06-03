# Carbon Emission Predictor - A prototype running on homogeneous Google Cloud Platform 
In the project, I am training an ARIMA model to conduct time series forecast of carbon emission with BigQuery. The data source is from www.watttime.org. The WattTime API provides access to real-time, forecast, and historical marginal emissions data for electric grids around the world. https://www.watttime.org/api-documentation/#introduction

## Project Overview
Even though the correlation between the Green house effects and global warming were already verified over three decades, not everyone concern about it except for some serious researchers, who won't seem to have enough fundings to continue their reseach in some key area like clean coal technolgy. As a result, the situation is getting worse since more and more developing countries are following the footsteps of developed country to use the fossil fuel which are more assessible to them economically. 

Be part of the global effort, it is opportunity for us to contribute our knowledge to take calculated risk to win. In this exercise, we will provide a MVP prototype to showcase how we can predict the carbon foot print per specific region on the homogeneous Google Cloud Platform with historical data retrieving with from wattTime company API. 

The next step is to let everyone know their carbon foot print of the power grids they are using such that they can leverage the Google smart home devices etc. to minimise net Carbon emission. 

## Architecture
![image](https://user-images.githubusercontent.com/11746291/120589268-972ba580-c406-11eb-8614-6a9b0f717fc8.png)

## USE CASE
For a recent project I needed to find an efficient way to extract data from API’s and load the response into a database residing in the cloud. As many of the energy and environment related Platforms are going online and expose their data services as APIs, the following use case is used for this project 
1. Google Cloud Serverless Function periodically calls API and saves JSON data file to storage bucket via cloud scheduler. 
2. BigQuery Data Transfer service automatically picks up  and loads .json files into the database table via the Pub/Sub triggeres.

## Serverless Function

![image](https://user-images.githubusercontent.com/11746291/120590542-ac093880-c408-11eb-90ed-35d5b8d08d64.png)

1. main.py
---------------------------------------------------------------------------------------------------------------
import base64
import requests 
import json 
import google.cloud 
from requests.auth import HTTPBasicAuth
from datetime import date, timedelta
from google.cloud import storage

def get_watttimes_data():
  login_url = 'https://api2.watttime.org/v2/login'
  token = requests.get(login_url, auth=HTTPBasicAuth('yourid', 'yourpassword')).json()['token']
  data_url = 'https://api2.watttime.org/v2/data'
  headers = {'Authorization': 'Bearer {}'.format(token)}
  params = {'ba': 'CAISO_ZP26', 
          'starttime': '2019-01-20T16:00:00-0800', 
          'endtime': '2019-02-20T16:15:00-0800'}
  rsp = requests.get(data_url, headers=headers, params=params)
  results = json.loads(rsp.text) 
  return (results)

def fetch_and_writeto_gcpstorage():
  #ction = base64.b64decode(data['data']).decode('utf-8') # retrieve pubsub message
    # ...
  storage_client=storage.Client()
  yesterday = date.today() - timedelta(1)
  yesterday = str(yesterday) [:10]
  #if (action == "download!"): # work is conditional on message content
  parsed=get_watttimes_data()
  payload = '\n'.join(json.dumps(item) for item in parsed)
  file_name = "wattimedata_{}.json".format(yesterday.replace("-", ""))
  storage_client.get_bucket("gcf-sources-json-us-central1") \
    .blob(file_name) \
    .upload_from_string(payload)

fetch_and_writeto_gcpstorage()

2. requirments.txt
---------------------------------------------------------------------------------------------------------------
google-cloud
google-cloud-bigquery
google-cloud-storage

## Cloud Scheduler



### [Checkout The Step-By-Step Tutorial](https://towardsdatascience.com/deploy-to-google-cloud-run-using-github-actions-590ecf957af0)

## Set Up
In order to deploy this project on your own you just need to take the following steps.

### 1. Create Service Account
The first step will be to create a service account by going to your [GCP Console Service Account Admin](https://console.cloud.google.com/iam-admin/serviceaccounts).

After which will need to give the service account the following roles.
 - Cloud Build Service Account
 - Cloud Build Editor
 - Service Account User
 - Viewer

### 2. Create Github Secrets
You will next need to navigate to the Settings Dashboard where you can add the following Github secrets. For this repo the link will be the following if you want to navigate directly to the location for your repo.


https://github.com/dylanroy/google-cloud-run-github-actions/settings/secrets

Here we setup our Github secrets:  
 - **GCP_CREDENTIALS** - This is your service account credentials that you will need to generate in the Google Cloud Console.  
 - **GCP_EMAIL** - This is the email that identifies the service account that you have provided credentials for in the secret labeled GCP_CREDENTIALS.
 - **GCP_PROJECT** - Your Google Project that you will deploying to Cloud Run.  
 - **GCP_APPLICATION** - Your Google service account application name for your Cloud Run service.

## Resources
 - [GCP Console Service Account Admin](https://console.cloud.google.com/iam-admin/serviceaccounts)
