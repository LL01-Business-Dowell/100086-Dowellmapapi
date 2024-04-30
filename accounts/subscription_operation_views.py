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

def delete_data(api_key,fil , payment=False):
    # url = "https://74.50.86.117/db_api/crud/"
    url = "https://datacube.uxlivinglab.online/db_api/crud/"

    payload = {
                        "api_key":api_key,
                        "operation":"delete",
                        "db_name":"dowell_map_trash_collction_app",
                        "coll_name":"trash_can_locs",
                        "query": fil,
                        "payment":payment
                        }

    content_length = len(json.dumps(payload))

    # Include the "Content-Length" header in your request
    # headers = {"Content-Length": str(content_length)}
    headers = {"Content-Type": "application/json", "Content-Length": str(len(payload))}
    r=requests.delete(url,json=payload)
    # print("data ------------->",payload)
    # print("response.status------------->",r.status_code)
    # print("r.text------------->",r.text)
    # print("r.message------------->",r.message)
    if r.status_code == 201 or r.status_code == 200 or r.status_code == 405:
        raw_data =  json.loads(r.text)
        res_data = {"status_code":r.status_code, "text":raw_data['message'], "success":True}
        # raw_keys = raw_data.keys()
        # print("raw_data------------->",raw_data)
    else:
        raw_data =  json.loads(r.text)
        res_data = {"success":False, "status_code":r.status_code, "text":raw_data['message']}
    return res_data

def update_data(api_key,id,data,   payment=False ):
    # url = "https://74.50.86.117/db_api/crud/"
    url = "https://datacube.uxlivinglab.online/db_api/crud/"
        # print("concat_data ==> ", concat_data)
    # print("concat_data ==> ", concat_data)
    payload = {
                        "api_key":api_key,
                        "operation":"update",
                        "db_name":"dowell_map_trash_collction_app",
                        "coll_name":"trash_can_locs",
                        "query": {"_id": id },
					    "update_data": data,
					    "payment":payment
                        }

    content_length = len(json.dumps(payload))

    # Include the "Content-Length" header in your request
    # headers = {"Content-Length": str(content_length)}
    headers = {"Content-Type": "application/json", "Content-Length": str(len(payload))}
    r=requests.put(url,json=payload)
    # print("data ------------->",payload)
    # print("response.status------------->",response.status)
    # print("r.text------------->",r.text)
    # print("r.message------------->",r.message)
    if r.status_code == 201 or r.status_code == 200:
        raw_data =  json.loads(r.text)
        res_data = {"status_code":r.status_code, "text":raw_data['message'], "success":True}
        # raw_keys = raw_data.keys()
        # print("raw_data------------->",raw_data)
    else:
        raw_data =  json.loads(r.text)
        res_data = {"success":False, "status_code":r.status_code, "text":raw_data['message']}
    return res_data
class SubscriptionOperations(APIView):
    def post(self, request, format=None):
        api_key = self.request.query_params.get("api_key")
        print('data ', request.data)
        response_list = list()
        dat= request.data
        workspace_id = dat['workspace_id']
        lat = dat['lat']
        long_ = dat['long']
        qr_code = dat['qr_code']


        data = {
            "workspace_id": workspace_id,
            "lat":lat,
            "long": long_,
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
class SubscriptionDeleteOperations(APIView):
    def post(self, request, format=None):
        error_message = "Kindly cross check the payload and parameters. If problem persists contact your admin"
        try:
            api_key = self.request.query_params.get("api_key")
            # api_key = ""
            myDict = request.data
            workspace_id = ""
            qr_code = ""
            culprit_dict = {}
            payment =  False
            if "payment" in myDict:
                payment = myDict['payment']
            if "workspace_id" in myDict:
                workspace_id = myDict['workspace_id']
            if "qr_code" in myDict:
                qr_code = myDict['qr_code']
            if len(qr_code):
                culprit_dict["qr_code"] = qr_code
            if len(workspace_id):
                culprit_dict["workspace_id"] = workspace_id
            res = delete_data(api_key,culprit_dict , payment)
            if not res['success']:
                error_message = res['text']
                raise CustomError(error_message)
            return Response(res,status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)

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