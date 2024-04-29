from django.shortcuts import render
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import datetime
import json
      
        
def insert_data(api_key, data, payment=False):
    # url = "https://74.50.86.117/db_api/crud/"
    url = "https://datacube.uxlivinglab.online/db_api/crud/"
    ts = datetime.datetime.now().timestamp()
    time_data = {"create_time_stamp": str(ts)}
    data.update(time_data)
    payload = {
        "api_key": api_key,
        "operation": "insert",
        "db_name": "dowell_map_trash_collction_app",
        "coll_name": "trash_can_locs",
        "data": data,
    }

    content_length = len(json.dumps(payload))

    # Include the "Content-Length" header in your request
    # headers = {"Content-Length": str(content_length)}
    headers = {"Content-Type": "application/json",
               "Content-Length": str(len(payload))}
    r = requests.post(url, json=payload)
    # print("data ------------->", payload)
    # print("response.status------------->",response.status)
    # print("r.text------------->",r.text)
    # print("r.message------------->",r.message)
    if r.status_code == 201 or r.status_code == 200:
        raw_data = json.loads(r.text)
        res_data = {"status_code": r.status_code,
                    "text": raw_data['message'], "success": True}
        # raw_keys = raw_data.keys()
        # print("raw_data------------->", raw_data)
    else:
        raw_data = json.loads(r.text)
        res_data = {"success": False, "status_code": r.status_code,
                    "text": raw_data['message']}
    return res_data


def get_data(api_key, workspace_id, fil=False, payment=False):
    # url = "https://74.50.86.117/db_api/crud/"
    url = "https://datacube.uxlivinglab.online/db_api/crud/"
    data = {
        "api_key": api_key,
        "operation": "fetch",
        "db_name": "dowell_map_trash_collction_app",
        "coll_name": "trash_can_locs",
        # "filters":json.dumps({"name":{"$regex":substr}})
        "filters": json.dumps({"workspace_id": workspace_id}),
    }
    if fil:
        data["filters"] = json.dumps(fil)

    wanted_dets = list()

    content_length = len(json.dumps(data))

    # Include the "Content-Length" header in your request
    # headers = {"Content-Length": str(content_length)}
    headers = {"Content-Type": "application/json",
               "Content-Length": str(len(data))}
    r = requests.get(url, data=data)
    # print("data ------------->", data)
    # print("response.status------------->",response.status)
    # print("r.text------------->",r.text)
    # print("r.message------------->",r.message)
    if r.status_code == 201 or r.status_code == 200:
        raw_data = json.loads(r.text)['data']
        res_data = {"data": raw_data, "success": True}
        # raw_keys = raw_data.keys()
        # print("raw_data------------->", raw_data)
    else:
        res_data = {"success": False, "status_code": r.status_code,
                    "text": json.loads(r.text)['message']}
    return res_data



class SubscriptionOperations(APIView):
    def post(self, request, format=None):
        api_key = self.request.query_params.get("api_key")
        print('data ', request.data)
        response_list = list()
        dat= request.data
        workspace_id = dat['workspace_id']
        lat = dat['lat']
        long = dat['long']
        qr_code = dat['qr_code']
        
        
        data = {
            "workspace_id": workspace_id,
            "lat":lat,
            "long": long,
            "qr_code": qr_code
        }
        print('api_key ', api_key)
        print('this is data ', data)
        res = insert_data(api_key, data)
        response_list.append(res)
        print('response',response_list)
        return Response(response_list)
        
        
        
        
        
    def get(self, request, format=None):
        api_key = self.request.query_params.get("api_key")
        response_list = list()
        dat= request.data
        workspace_id = dat['workspace_id']
        # lat = dat['lat']
        # long = dat['long']
        # qr_Code = dat["qr_code"]
        
        
        # data = {
        #     workspace_id: workspace_id,
        #     lat:lat,
        #     long: long,
        #     qr_Code: qr_Code
        # }
        
        
        res = get_data(api_key, workspace_id)
        response_list.append(res)
        print('results ', response_list)
        return Response(response_list)
    
    
    
class SubscriptionsGetOperations(APIView):
    def post(self, request, format=None):
        api_key = self.request.query_params.get("api_key")
        response_list = list()
        dat= request.data
        workspace_id = dat['workspace_id']
        # lat = dat['lat']
        # long = dat['long']
        # qr_Code = dat["qr_code"]
        
        
        # data = {
        #     workspace_id: workspace_id,
        #     lat:lat,
        #     long: long,
        #     qr_Code: qr_Code
        # }
        
        
        res = get_data(api_key, workspace_id)
        response_list.append(res)
        print('results ', response_list)
        return Response(response_list)