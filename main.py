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
