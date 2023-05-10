import json
import requests
import os
import pandas as pd
from django.conf import settings
import haversine as hs
BASE_DIR = settings.BASE_DIR
static_path = os.path.join(BASE_DIR, 'static')
directory =  os.path.join(BASE_DIR, 'json_data')
id_directory =  os.path.join(BASE_DIR, 'json__id_data')
plc_id_file_name =  os.path.join(id_directory, "id_json_data.json")
##Insertion of data
def insert_data(data):
    #dowellconnectionfunction

    url = "http://100002.pythonanywhere.com/"
#searchstring="ObjectId"+"("+"'"+"6139bd4969b0c91866e40551"+"'"+")"
    payload = json.dumps({
    "cluster": "dowellmap",
    "database": "dowellmap",
    "collection": "my_map",
    "document": "my_map",
    "team_member_ID": "1164",
    "function_ID": "ABCDE",
    "command": "insert",
    "field": data,
        # "test_data" : "test_data",
    "update_field": {
        "order_nos": 21
        },
    "platform": "bangalore"
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    response_dict= json.loads(response.text)
    print(response.text)
    return response_dict
###############################################3
######

#Fetch Data From Mongo
def fetch_from_mongo():
    url = "http://100002.pythonanywhere.com/"
    headers = {'content-type': 'application/json'}

    payload = {
    "cluster": "dowellmap",
    "database": "dowellmap",
    "collection": "my_map",
    "document": "my_map",
    "team_member_ID": "1164",
    "function_ID": "ABCDE",
    "command": "fetch",
    "field": {
        
        },
    "update_field": {
        "order_nos": 21
        },
    "platform": "bangalore"
    }
    data = json.dumps(payload)
    response = requests.request("POST", url, headers=headers, data=data)
    # print(response.text)
    result = json.loads(response.text)
    # print(result['isSuccess'])
    # print(type(result['data']))
    # print(result['data'])
    return result['data']
#Fetch Data from Json
def fetch_from_json():
    
    # file_path = 'json_data\sample.json'
    n= len(os.listdir(directory))
    # isExist = os.path.exists(file_path)
    # print(isExist)
    # print(n)
    json_data_lists = list()
    for i in range(1,n+1):
        temp_file_name =  os.path.join(directory, "rec"+str(i)+".json")
        isTempExist = os.path.exists(temp_file_name)
        sizee = os.path.getsize(temp_file_name)
        file_stats = os.stat(temp_file_name)
        # print("i ", i)    
        # print("sizee",sizee)
        # print(f"file_stats in bytes is {file_stats.st_size}")
        # print(f"file_stats in megabytes is {file_stats.st_size / (1024 * 1024)}")
        if isTempExist:
            with open(temp_file_name, 'r') as openfile:
            # Reading from json file
                json_object = json.load(openfile)
                # print("Round ===================")
                # print(json_object)
                # print("Round ===================")

            json_data_lists.append(json_object)
    # print(json_data_lists)
    return json_data_lists
### Wtiter to json
def write_json_data(file_name, new_data):
    try:
        isExist = os.path.exists(file_name)
        data = list()
        data_ids = list()
        if isExist:
            #get old data and combine
            with open(file_name, 'r') as openfile:
    
    #     # Reading from json file
                old_data = json.load(openfile)
            old_data_list = old_data['data']
            data = old_data_list + new_data

            
        else:
            data = new_data
        for i in data:
            if 'placeId' in i:
                if i['placeId'] not in data_ids:
                    data_ids.append(i['placeId'])
            if 'place_id' in i:
                if i['place_id'] not in data_ids:
                    data_ids.append(i['place_id'])
            #insert in new file
        json_object = json.dumps(data, indent=4)
        with open(file_name, "w") as outfile:
            outfile.write(json_object)
        if len(data_ids):
            id_data = {"data":data_ids}
            json_object = json.dumps(id_data, indent=4)
            with open(plc_id_file_name, "w") as outfile:
                outfile.write(json_object)

        return True
    except:
        return False



#Create Data to Json
def create_json_data():
    #Check for number of records

    n= len(os.listdir(directory))
    print("n==",n)
    
    #Collect Present ids in Json
    json_data_lists = list()
    json_data_sizes = dict()
    if n:
        for i in range(1,n+1):
            temp_file_name = os.path.join(directory, "rec"+str(i)+".json")
            sizee = os.path.getsize(temp_file_name)
            file_stats = os.stat(temp_file_name)
            print("i ", i)    
            print("sizee",sizee)
            print(f"file_stats in bytes is {file_stats.st_size}")
            print(f"file_stats in megabytes is {file_stats.st_size / (1024 * 1024)}")
            json_data_sizes[temp_file_name] = file_stats.st_size / (1024 * 1024)

            with open(temp_file_name, 'r') as openfile:
            # Reading from json file
                json_object = json.load(openfile)
                # print("Round ===================")
                # print(json_object)
                # print("Round ===================")

            json_data_lists.append(json_object)
        # print("json data", json_data_lists)
        # print("json data sizess", json_data_sizes)
    json_data_ids = list()
    for i in json_data_lists:
        for t in i['data']:
            json_data_ids.append(t['_id'])
    # print("json ids",json_data_ids)
    #Collect Present ids in Mongo
    mongo_data = fetch_from_mongo()
    mongo_df = pd.DataFrame.from_dict(mongo_data)
    mongo_data_ids = [i['_id'] for i in mongo_data ]
    #Get missing numbers 
    missing_ids = set(mongo_data_ids ).difference(set(json_data_ids))
    print("missing ids",missing_ids)
    # print(mongo_df.head())
    missing_data_df = mongo_df.loc[mongo_df['_id'].isin(mongo_data_ids)]
    missing_data_list = missing_data_df.to_dict('records')
    print(missing_data_df)
    print("------------------------------------------------->>>>>>>>>>>>>>>>>>>>>>")
    print(missing_data_list)
    #Write on last json 
    culprit_file_name =  os.path.join(directory, "rec"+str(n)+".json")
    new_file_name = ""
    if  n == 0 or json_data_sizes[culprit_file_name] >= 100:
        new_file_name =  os.path.join(directory, "rec"+str(n+1)+".json")
    else:
        new_file_name = culprit_file_name
    
    isHandled=write_json_data(new_file_name, missing_data_list)
    print("ishHandled =====> ", isHandled)
    return isHandled

def get_unique(place_id_list):
    #Fetch all place ids
    isExist = os.path.exists(plc_id_file_name)
    if isExist:
        with open(plc_id_file_name, 'r') as openfile:
            # Reading from json file
                json_object_ids = json.load(openfile)
        json_id_list = json_object_ids['data']
        #Do difference in sets
        distinct_list = list(set(place_id_list).difference(set(json_id_list)) )
         # return list distince
    
        return distinct_list
    else:
        return []
### Get differremce in distances
def get_difference(latt1,lonn1, latt2,lonn2):
    loc1 = (latt1,lonn1)
    loc2 = (latt2, lonn2)
    distance = hs.haversine(loc1,loc2, unit=hs.Unit.METERS)
    return distance
def split_string(loc_str1, loc_str2):
    print("loc_str 1", loc_str1)
    print("loc_str 2", loc_str2)

    if loc_str1 == '' or loc_str1 == ' ':
        loc_str1 = '0 , 0'
    if loc_str2 == '' or loc_str2 == ' ':
        loc_str2 = '0 , 0'
    offset1 = loc_str1.find(',')
    latt1 = float(loc_str1[:offset1].strip())
    lonn1 = float(loc_str1[offset1+1:].strip())
    print("latt ",latt1)
    print("lonn ",lonn1)
    offset2 = loc_str2.find(',')
    latt2 = float(loc_str2[:offset2].strip())
    lonn2 = float(loc_str2[offset2+1:].strip())
    print("latt ",latt2)
    print("lonn ",lonn2)
    hav_distance = get_difference(latt1,lonn1, latt2,lonn2)
    return hav_distance

 
   
# fetch_from_mongo()
# fetch_from_json()
# create_json_data()