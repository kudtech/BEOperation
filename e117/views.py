from django.shortcuts import render
from beweb.views import user_authenticate,execsys
from django.views.generic import View
from datetime import datetime
import random
import json
import requests

class SaveE117Job(View):
    def get(self,request,*args, **kwargs): 
        print('+++++++++++++++++++')
        print(request.GET)
        print('+++++++++++++++++++')
        job_id=request.GET.get('job_number')        
        created_by=request.user.username
        data=execsys(request.user.username)
        section=data['section']
        workorder_number=request.GET.get('workorder_number','wo20200317112368775')
        client_id="ci"+datetime.now().strftime("%Y%m%d%H%M") + str(random.randrange(000000, 100000))
        client_name=request.GET.get('customer_name')
        property_address=request.GET.get('property_address')
        client_phone=request.GET.get('customer_phone')
        owner_name=request.GET.get('property_owner_name')
        owner_address=request.GET.get('property_owner_address')
        save_client(client_id,client_name,property_address,client_phone,owner_name,owner_address,created_by)
        save_e117(job_id,created_by,section,workorder_number,client_id)
        return render(request,'beweb/job/notification.html')


def save_client(client_id,client_name,property_address,client_phone,owner_name,owner_address,created_by):
    user, token = user_authenticate(created_by)
    url = 'http://172.20.0.70:8087/beapi/clientpost/'
    headers = {'Authorization': "Token "+token +"", "Content-Type": "application/json"
    }
    data = {
        "client_id":client_id,
        "client_name": client_name,
        "property_address": property_address,
        "client_phone": client_phone,
        "owner_name": owner_name,
        "owner_address": owner_address
    }
    data = json.dumps(data)
    r = requests.post(url=url, data=data, headers=headers) 
    response_data = r.json()
    client_name = client_name
    return client_name


def save_e117(job_id,created_by,section,workorder_number,client_id):
    user,token=user_authenticate(created_by)
    created_on=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url = 'http://172.20.0.70:8087/beapi/e117post/'
    headers = {'Authorization': "Token "+token + "", "Content-Type": "application/json"}
    data = {
        "e117_id":"e"+datetime.now().strftime("%Y%m%d%H%M") + str(random.randrange(000000, 100000)),
        "created_by": created_by,
        "job": job_id,
        "created_on": datetime.now().strftime("%Y%m%d%H%M"),
        "client_inspection_type": 'E117',
        "e117client": client_id
    }
    data = json.dumps(data)
    r = requests.post(url=url,data=data, headers=headers) 
    response_data = r.json()
    createdby = created_by
    return createdby




