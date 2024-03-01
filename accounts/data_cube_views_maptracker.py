from django.shortcuts import render
import requests
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, JsonResponse
import datetime
# Used to track messages
error_message = ""
database_name = "dowellmap_locations"
collection_name = "tracked_loctions_data"


class CustomError(Exception):
    pass
### MAJOR FUNCTIONS ###


def insert_data(api_key, data, payment=False):
    # url = "https://74.50.86.117/db_api/crud/"
    url = "https://datacube.uxlivinglab.online/db_api/crud/"
    ts = datetime.datetime.now().timestamp()
    time_data = {"create_time_stamp": str(ts)}
    data.update(time_data)
    payload = {
        "api_key": api_key,
        "operation": "insert",
        "db_name": database_name,
        "coll_name": collection_name,
        "data": data,
        "payment": payment
    }

    content_length = len(json.dumps(payload))

    # Include the "Content-Length" header in your request
    # headers = {"Content-Length": str(content_length)}
    headers = {"Content-Type": "application/json",
               "Content-Length": str(len(payload))}
    r = requests.post(url, json=payload)
    print("data ------------->", payload)
    # print("response.status------------->",response.status)
    # print("r.text------------->",r.text)
    # print("r.message------------->",r.message)
    if r.status_code == 201 or r.status_code == 200:
        raw_data = json.loads(r.text)
        res_data = {"status_code": r.status_code,
                    "text": raw_data['message'], "success": True}
        # raw_keys = raw_data.keys()
        print("raw_data------------->", raw_data)
    else:
        raw_data = json.loads(r.text)
        res_data = {"success": False, "status_code": r.status_code,
                    "text": raw_data['message']}
    return res_data


def get_data(api_key, fil=False, payment=False):
    # url = "https://74.50.86.117/db_api/crud/"
    url = "https://datacube.uxlivinglab.online/db_api/crud/"
    data = {
        "api_key": api_key,
        "operation": "fetch",
        "db_name": database_name,
        "coll_name": collection_name,
        "payment": payment
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
    print("data ------------->", data)
    # print("response.status------------->",response.status)
    # print("r.text------------->",r.text)
    # print("r.message------------->",r.message)
    if r.status_code == 201 or r.status_code == 200:
        raw_data = json.loads(r.text)['data']
        res_data = {"data": raw_data, "success": True}
        # raw_keys = raw_data.keys()
        print("raw_data------------->", raw_data)
    else:
        res_data = {"success": False, "status_code": r.status_code,
                    "text": json.loads(r.text)['message']}
    return res_data


def update_data(api_key, id, data, update_fields, payment=False):
    # url = "https://74.50.86.117/db_api/crud/"
    url = "https://datacube.uxlivinglab.online/db_api/crud/"
    concat_data = data
    old_data = get_data(api_key, fil={"_id": id})
    for i in update_fields:
        if i in ["users_list", "team_list"]:
            concat_data[i] = list(set(old_data["data"][0][i] + data[i]))
        if i == "teams_list":
            if "teams" in data:
                for k in data[i]:
                    if k in old_data["teams"]:
                        concat_data["teams"][k] = list(
                            set(old_data["data"][0]["teams"][k] + data["teams"][k]))
                    else:
                        concat_data["teams"][k] = data["teams"][k]
        # print("concat_data ==> ", concat_data)
    print("concat_data ==> ", concat_data)
    payload = {
        "api_key": api_key,
        "operation": "update",
        "db_name": database_name,
        "coll_name": collection_name,
        "query": {"_id": id},
        "update_data": concat_data,
        "payment": payment
    }

    content_length = len(json.dumps(payload))

    # Include the "Content-Length" header in your request
    # headers = {"Content-Length": str(content_length)}
    headers = {"Content-Type": "application/json",
               "Content-Length": str(len(payload))}
    r = requests.put(url, json=payload)
    print("data ------------->", payload)
    # print("response.status------------->",response.status)
    # print("r.text------------->",r.text)
    # print("r.message------------->",r.message)
    if r.status_code == 201 or r.status_code == 200:
        raw_data = json.loads(r.text)
        res_data = {"status_code": r.status_code,
                    "text": raw_data['message'], "success": True}
        # raw_keys = raw_data.keys()
        print("raw_data------------->", raw_data)
    else:
        raw_data = json.loads(r.text)
        res_data = {"success": False, "status_code": r.status_code,
                    "text": raw_data['message']}
    return res_data


def delete_data(api_key, fil, payment=False):
    # url = "https://74.50.86.117/db_api/crud/"
    url = "https://datacube.uxlivinglab.online/db_api/crud/"

    payload = {
        "api_key": api_key,
        "operation": "delete",
        "db_name": database_name,
        "coll_name": collection_name,
        "query": fil,
        "payment": payment
    }

    content_length = len(json.dumps(payload))

    # Include the "Content-Length" header in your request
    # headers = {"Content-Length": str(content_length)}
    headers = {"Content-Type": "application/json",
               "Content-Length": str(len(payload))}
    r = requests.delete(url, json=payload)
    print("data ------------->", payload)
    print("response.status------------->", r.status_code)
    print("r.text------------->", r.text)
    # print("r.message------------->",r.message)
    if r.status_code == 201 or r.status_code == 200 or r.status_code == 405:
        raw_data = json.loads(r.text)
        res_data = {"status_code": r.status_code,
                    "text": raw_data['message'], "success": True}
        # raw_keys = raw_data.keys()
        print("raw_data------------->", raw_data)
    else:
        raw_data = json.loads(r.text)
        res_data = {"success": False, "status_code": r.status_code,
                    "text": raw_data['message']}
    return res_data
### VIEWS ###


class CreateWorkspace(APIView):
    """
    Create a workspace
    """

    def get(self, request, format=None):
        return JsonResponse({"message": "Kindly use POST request"})
#  master:{
#     workspace_id
#     user_name:
#     users_list:[]
#     team_list:[]
#     teams:{
#         team1:[],
#         team2:[],
#         team3:[],
#     }
# }

    def post(self, request):
        error_message = "Kindly cross check the payload and parameters. If problem persists contact your admin"
        try:
            api_key = self.request.query_params.get("api_key")
            # api_key=""
            myDict = request.data
            username = myDict['username']
            workspace_id = myDict['workspace_id']

            payment = False
            users_list = []
            team_list = []
            teams = []
            if "payment" in myDict:
                payment = myDict['payment']
            if "users_list" in myDict:
                users_list = myDict['users_list']
            if "team_list" in myDict:
                team_list = myDict['team_list']
            if "teams" in myDict:
                teams = myDict['teams']

            check_res = get_data(
                api_key, {"username": username, "workspace_id": workspace_id, "doc_type": "master"}, payment)
            res = {}
            if len(check_res['data']) == 0:
                data = {
                    "username": username,
                    "workspace_id": workspace_id,
                    "doc_type": "master",
                    "users_list": users_list,
                    "team_list": team_list,
                    "teams": teams,
                }

                res = insert_data(api_key, data)
            else:
                error_message = "Workspace exists already!"
                raise CustomError(error_message)
            # wanted_dets.extend(get_data(payload))
                # res = {"Coords": "Kindly wait api in maintenance. Thank you for your patience"}
            return Response(res, status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)


class GetWorkspace(APIView):
    """
    Get the details about the workspace
    """

    def get(self, request, format=None):
        return JsonResponse({"message": "Kindly use POST request"})

    def post(self, request):
        error_message = "Kindly cross check the payload and parameters. If problem persists contact your admin"
        try:
            api_key = self.request.query_params.get("api_key")
            wanted_dets = list()
            myDict = request.data
            payment = False
            if "payment" in myDict:
                payment = myDict['payment']
            if "filters" in myDict:
                res = get_data(api_key, myDict['filters'], payment)
            else:
                res = get_data(api_key, payment)
            if res['success']:
                wanted_dets = res['data']
            else:
                error_message = res['text']
                raise CustomError(res['text'])
            # wanted_dets.extend(get_data(payload))
            res = {"data": wanted_dets}
            # res = {"Coords": "Kindly wait api in maintenance. Thank you for your patience"}
            return Response(res, status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)


class UpdateWorkspace(APIView):
    """
    List all countries, or create a new country.
    """

    def get(self, request, format=None):
        return JsonResponse({"message": "Kindly use POST request"})

    def post(self, request):
        error_message = "Kindly cross check the payload and parameters. If problem persists contact your admin"
        try:
            api_key = self.request.query_params.get("api_key")
            # api_key = ""
            myDict = request.data
            username = myDict['username']
            workspace_id = myDict['workspace_id']
            update_fields = myDict['update_fields']
            update_data = myDict['update_data']
            if "teams" in update_fields:
                if "team_list" not in update_fields:
                    raise CustomError(
                        "Team list field missing for the teams sent.")
                if len(update_data['team_list']) != len(update_data['teams']):
                    raise CustomError(
                        "Some team names do not match up with the list given. Compare your team list and the teams sent")
            payment = False
            if "payment" in myDict:
                payment = myDict['payment']
            check_res = get_data(
                api_key, {"username": username, "workspace_id": workspace_id}, payment)
            res = {}
            if len(check_res['data']) == 0:
                error_message = "Workspace does not exist!"
                raise CustomError(error_message)

            else:
                doc_id = False
                for i in check_res["data"]:
                    res = {}
                    if i['doc_type'] == "master":
                        doc_id = i["_id"]
                        break
                if doc_id:
                    # update_data(api_key, id, data, update_fields, payment=False)
                    res = update_data(
                        api_key, doc_id, update_data, update_fields, payment)
                    if not res['success']:
                        error_message = res['text']
                        raise CustomError(error_message)
                else:
                    error_message = "A master record for username and workspace id sent does not exist. Contact the admin for further guidance."
                    raise CustomError(error_message)
            return Response(res, status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)


class DeleteWorkspace(APIView):
    """
    List all countries, or create a new country.
    """

    def get(self, request, format=None):
        return JsonResponse({"message": "Kindly use POST request"})

    def post(self, request):
        error_message = "Kindly cross check the payload and parameters. If problem persists contact your admin"
        try:
            api_key = self.request.query_params.get("api_key")
            # api_key = ""
            myDict = request.data
            username = myDict['username']
            workspace_id = myDict['workspace_id']
            payment = False
            if "payment" in myDict:
                payment = myDict['payment']
            res = delete_data(
                api_key, {"username": username, "workspace_id": workspace_id}, payment)
            if not res['success']:
                error_message = res['text']
                raise CustomError(error_message)
            return Response(res, status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)
## Location Data ###


class CreateLocationData(APIView):
    """
    Create Location data
    """

    def get(self, request, format=None):
        return JsonResponse({"message": "Kindly use POST request"})
# slave:{
#     lat:
#     lon:
#     time_stamp:
#     user_device:
#     user_name:
#     team_list:
#     master_workspace_id
#     master_username
# time_of_entry

# }
    def post(self, request):
        error_message = "Kindly cross check the payload and parameters. If problem persists contact your admin"
        try:
            api_key = self.request.query_params.get("api_key")
            # api_key=""
            myDict = request.data
            username = myDict['username']
            workspace_id = myDict['workspace_id']
            team_status = myDict["team_status"]
            lat = myDict['lat']
            lon = myDict['lon']
            timestamp = myDict['timestamp']
            # user_device = myDict['user_device']
            team_list = []
            master_username = myDict['master_username']
            payment = False
            if "payment" in myDict:
                payment = myDict['payment']
            if "team_list" in myDict:
                team_list = myDict['team_list']

            check_res = get_data(
                api_key, {"username": username, "timestamp": timestamp, "doc_type": "slave"})
            res = {}
            if len(check_res['data']) == 0:
                data = {}
                if team_status:
                    data = {
                        "username": username,
                        "workspace_id": workspace_id,
                        "doc_type": "slave",
                        "lat": lat,
                        "lon": lon,
                        "timestamp": timestamp,
                        "team_status": True,
                        "team_list": team_list
                    }
                else:

                    data = {
                        "username": username,
                        "workspace_id": workspace_id,
                        "doc_type": "slave",
                        "lat": lat,
                        "lon": lon,
                        "timestamp": timestamp,
                        "team_status": False
                    }

                res = insert_data(api_key, data)
            else:
                error_message = "Location already inserted!"
                raise CustomError(error_message)
            # wanted_dets.extend(get_data(payload))
                # res = {"Coords": "Kindly wait api in maintenance. Thank you for your patience"}
            return Response(res, status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)


class GetLocationData(APIView):
    """
    List all countries, or create a new country.
    """

    def get(self, request, format=None):
        return JsonResponse({"message": "Kindly use POST request"})

    def post(self, request):
        error_message = "Kindly cross check the payload and parameters. If problem persists contact your admin"
        try:
            api_key = self.request.query_params.get("api_key")
            wanted_dets = list()
            myDict = request.data
            payment = False
            if "payment" in myDict:
                payment = myDict['payment']
            if "filters" in myDict:
                res = get_data(api_key, myDict['filters'], payment)
            else:
                res = get_data(api_key, payment)
            if res['success']:
                wanted_dets = res['data']
            else:
                error_message = res['text']
                raise CustomError(res['text'])
            # wanted_dets.extend(get_data(payload))
            res = {"data": wanted_dets}
            # res = {"Coords": "Kindly wait api in maintenance. Thank you for your patience"}
            return Response(res, status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)


class UpdateLocation(APIView):
    """
    List all countries, or create a new country.
    """

    def get(self, request, format=None):
        return JsonResponse({"message": "Kindly use POST request"})

    def post(self, request):
        error_message = "Kindly cross check the payload and parameters. If problem persists contact your admin"
        try:
            api_key = self.request.query_params.get("api_key")
            # api_key = ""
            myDict = request.data
            username = myDict['username']
            workspace_id = myDict['workspace_id']
            timestamp = myDict['timestamp']
            update_fields = myDict['update_fields']
            update_data = myDict['update_data']
            payment = False
            if "payment" in myDict:
                payment = myDict['payment']
            check_res = get_data(
                api_key, {"username": username, "workspace_id": workspace_id, "timestamp": timestamp}, payment)
            res = {}
            if len(check_res['data']) == 0:
                error_message = "Loction entry does not exist!"
                raise CustomError(error_message)

            else:
                doc_id = False
                for i in check_res["data"]:
                    res = {}
                    if i['doc_type'] == "slave":
                        doc_id = i["_id"]

                        if doc_id:
                            # update_data(api_key, id, data, update_fields, payment=False)
                            res = update_data(
                                api_key, doc_id, update_data, update_fields, payment)
                            if not res['success']:
                                error_message = res['text']
                                raise CustomError(error_message)

            return Response(res, status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)


class DeleteLocationData(APIView):
    """
    List all countries, or create a new country.
    """

    def get(self, request, format=None):
        return JsonResponse({"message": "Kindly use POST request"})

    def post(self, request):
        error_message = "Kindly cross check the payload and parameters. If problem persists contact your admin"
        try:
            api_key = self.request.query_params.get("api_key")
            # api_key = ""
            myDict = request.data
            filter = myDict["filter"]
            payment = False
            if "payment" in myDict:
                payment = myDict['payment']
            res = delete_data(
                api_key, filter, payment)
            if not res['success']:
                error_message = res['text']
                raise CustomError(error_message)
            return Response(res, status=status.HTTP_200_OK)
        except CustomError:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly cross check the payload and parameters or contact your admin", status=status.HTTP_400_BAD_REQUEST)
# Create
# Create master with workspace_id, username, teams,, users_list and in users_intemas
# master:{
#     workspace_id
#     user_name:
#     users_list:[]
#     team_list:[]
#     teams:{
#         team1:[],
#         team2:[],
#         team3:[],
#     }
# }


# Fetch by team, username, workspace_id


# Update team
# Update users in team
# Update users
# Delete team
# Delete users
# Delete master
# Create Slave with lat and lon , time stamp
# slave:{
#     lat:
#     lon:
#     time_stamp:
#     user_device:
#     user_name:
#     team_list:
#     master_workspace_id
#     master_username
# time_of_entry

# }
# Fetch by any of the above
# Delete
# Update
