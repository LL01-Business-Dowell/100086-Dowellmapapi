import requests
import json
import datetime

def insert_data(api_key, collection, data, payment=False):
    # url = "https://74.50.86.117/db_api/crud/"
    url = "https://datacube.uxlivinglab.online/db_api/crud/"
    ts = datetime.datetime.now().timestamp()
    time_data = {"create_time_stamp": str(ts)}
    data.update(time_data)
    payload = {
        "api_key": api_key,
        "operation": "insert",
        "db_name": "student_management",
        "coll_name": collection,
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


def get_data(api_key, collection, fil=False, payment=False):
    # url = "https://74.50.86.117/db_api/crud/"
    url = "https://datacube.uxlivinglab.online/db_api/crud/"
    data = {
        "api_key": api_key,
        "operation": "fetch",
        "db_name": "student_management",
        "coll_name": collection,
        # "filters":json.dumps({"name":{"$regex":substr}})
        "filters": json.dumps(fil),
    }

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
        print('Here is it...')
        res_data = {"success": False, "status_code": r.status_code,
                    "text": json.loads(r.text)['message']}
    return res_data