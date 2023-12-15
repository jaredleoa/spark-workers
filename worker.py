from flask import Flask
from flask import request
from flask import render_template
from google.cloud import secretmanager
import requests
import os
import json
app = Flask(__name__)


def access_secret_version(secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/856391429466/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')

    
@app.route("/")
def hello():
    return "Add workers to the Spark cluster with a POST request to add"

@app.route("/test")
def test():
    return(access_secret_version("compute-api-key"))

@app.route("/add",methods=['GET','POST'])
def add():
  if request.method=='GET':
      return render_template('adding_vm_form.html')
  else:
    token=access_secret_version("api")
    ret = addWorker(token,request.form['num'])
    return ret

def addWorker(token, num):
    with open('payload.json') as p:
      tdata=json.load(p)
    tdata['name']="slave1"+str(num)
    data=json.dumps(tdata)
    url='https://www.googleapis.com/compute/v1/projects/weighty-works-400314/zones/europe-west2-c/instances'
    headers={"Authorization": "Bearer "+token}
    resp=requests.post(url,headers=headers, data=data)
    if resp.status_code==200:     
      return "Done"
    else:
      print(resp.content)
      return "Error\n"+resp.content.decode('utf-8') + '\n\n\n'+data


if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8080')
