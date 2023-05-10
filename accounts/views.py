from django.shortcuts import render
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from datetime import datetime
from accounts import data_handlers as dh
import pandas as pd

# Create your views here.

def preparing_list_for_error_message(wanted_l):
    full_str ="[ " +', '.join([str(elem) for elem in wanted_l])+" ]"
    return full_str
def get_event_id():

    url="https://uxlivinglab.pythonanywhere.com/create_event"

    data={
        "platformcode":"FB" ,
        "citycode":"101",
        "daycode":"0",
        "dbcode":"pfm" ,
        "ip_address":"192.168.0.41", # get from dowell track my ip function
        "login_id":"lav", #get from login function
        "session_id":"new", #get from login function
        "processcode":"1",
        "location":"22446576", # get from dowell track my ip function
        "objectcode":"1",
        "instancecode":"100051",
        "context":"afdafa ",
        "document_id":"3004",
        "rules":"some rules",
        "status":"work",
        "data_type": "learn",
        "purpose_of_usage": "add",
        "colour":"color value",
        "hashtags":"hash tag alue",
        "mentions":"mentions value",
        "emojis":"emojis",
        "bookmarks": "a book marks"
    }

    r=requests.post(url,json=data)
    if r.status_code == 201:
        eventId= json.loads(r.text)['event_id'],
        return eventId
    else:
        return json.loads(r.text)['error']
def retrieve_details(results_1, plc_id, is_test_data):
    place_id_ = plc_id
    place_name = 'None'
    category = 'None'
    address = 'None'
    lng = 'None'
    lat = 'None'
    types = 'None'
    website = 'None'
    open_hrs = 'None'
    int_number = 'None'
    error = False
    eventId = get_event_id()
    if results_1['status'] == 'OK':
        results = results_1['result']
        status = results_1['status']
        if 'place_id' in results:
            # print(results['place_id'])
            place_id_ = results['place_id']
        if 'name' in results:
            # print(results['name'])
            place_name = results['name']
        if 'formatted_address' in results:
            # print(results['formatted_address'])
            address = results['formatted_address']
        if 'geometry' in results:
            # print(results['geometry']['location']['lng'])
            lng = results['geometry']['location']['lng']
            lat = results['geometry']['location']['lat']
        if 'types' in results:
            # print(results['types'])
            types = results['types']
            category = results['types']
        if 'website' in results:
            # print(results['website'])
            website = results['website']
        if 'international_phone_number' in results:
            # print(results['international_phone_number'])
            int_number = results['international_phone_number']
        if 'opening_hours' in results:
            # print(results['opening_hours']["weekday_text"])
            open_hrs = results['opening_hours']["weekday_text"]
    else:
        error = True
    template = {
    "placeId":place_id_,
    'place_name': place_name,
    'category': category,
    'address': address,
    'location_coord': str(lat) + " , "+str(lng),
    'day_hours': open_hrs,
    'phone': int_number,
    'website': website,
    "type_of_data": "scraped",
    "is_test_data": is_test_data,
        "eventId": eventId,
        "error": error
        }
    return template

class CustomError(Exception):
    pass
class GetPlaceDetails(APIView):
    """
    List all countries, or create a new country.
    """
    def get(self, request, format=None):
        return JsonResponse({"status":"All good"})
    def post(self, request):
        place_id = request.data.get('place_id')
        url='https://maps.googleapis.com/maps/api/place/details/json?placeid='+place_id+'&key=AIzaSyC_oMIdGvpBALKg6W6TPgpwVLb-viGwonY'


        try:
            # api_response = api_instance.send_transac_email(send_smtp_email)
            r=requests.get(url)
            # print(r.text)
            results = json.loads(r.text)
            # print("Type resultsa")
            # print(type(results))

            api_response_dict = {"res":results}

            return Response(results,status=status.HTTP_200_OK)
        except CustomError:


            return Response("No results for the place id: "+"place_id", status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("No results for the place id: "+"place_id", status=status.HTTP_400_BAD_REQUEST)
class GetPlaceDetailsList(APIView):
    """
    List all countries, or create a new country.
    """
    def get(self, request, format=None):
        # ll = [{"place_id":"EhdQUTM2K0hNLCBOYWlyb2JpLCBLZW55YSImOiQKCg2PPDr_FWtj6RUQChoUChIJp0lN2HIRLxgRTJKXslQCz_c","place_name":"PQ36+HM","category":["street_address"],"address":"PQ36+HM, Nairobi, Kenya","location_coord":"-1.2960625 , 36.7616875","day_hours":"None","phone":"None","website":"None","type_of_data":"scraped","is_test_data":True,"eventId":["FB1010000000000000000000003004"],"error":False}]
        # ll2 = {'html_attributions': [], 'result': {'address_components': [{'long_name': 'Nairobi', 'short_name': 'Nairobi', 'types': ['locality', 'political']}, {'long_name': 'Maziwa', 'short_name': 'Maziwa', 'types': ['sublocality_level_1', 'sublocality', 'political']}, {'long_name': 'Nairobi County', 'short_name': 'Nairobi County', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'Kenya', 'short_name': 'KE', 'types': ['country', 'political']}, {'long_name': '00600', 'short_name': '00600', 'types': ['postal_code']}], 'adr_address': 'kingara Road, <span class="street-address">opp kingara close behind Junction Mall</span>, <span class="postal-code">00600</span>, <span class="locality">Nairobi</span>, <span class="country-name">Kenya</span>', 'business_status': 'OPERATIONAL', 'current_opening_hours': {'open_now': True, 'periods': [{'close': {'date': '2023-04-23', 'day': 0, 'time': '2100'}, 'open': {'date': '2023-04-23', 'day': 0, 'time': '1100'}}, {'close': {'date': '2023-04-24', 'day': 1, 'time': '2100'}, 'open': {'date': '2023-04-24', 'day': 1, 'time': '1100'}}, {'close': {'date': '2023-04-25', 'day': 2, 'time': '2100'}, 'open': {'date': '2023-04-25', 'day': 2, 'time': '1100'}}, {'close': {'date': '2023-04-26', 'day': 3, 'time': '2100'}, 'open': {'date': '2023-04-26', 'day': 3, 'time': '1100'}}, {'close': {'date': '2023-04-27', 'day': 4, 'time': '2100'}, 'open': {'date': '2023-04-27', 'day': 4, 'time': '1100'}}, {'close': {'date': '2023-04-21', 'day': 5, 'time': '2100'}, 'open': {'date': '2023-04-21', 'day': 5, 'time': '1100'}}, {'close': {'date': '2023-04-22', 'day': 6, 'time': '2100'}, 'open': {'date': '2023-04-22', 'day': 6, 'time': '1100'}}], 'weekday_text': ['Monday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Tuesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Wednesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Thursday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Friday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Saturday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Sunday: 11:00\u202fAM\u2009–\u20099:00\u202fPM']}, 'delivery': True, 'dine_in': True, 'formatted_address': 'kingara Road, opp kingara close behind Junction Mall, Nairobi, Kenya', 'formatted_phone_number': '0742 894700', 'geometry': {'location': {'lat': -1.2960063, 'lng': 36.7616708}, 'viewport': {'northeast': {'lat': -1.294604919708498, 'lng': 36.7631173802915}, 'southwest': {'lat': -1.297302880291502, 'lng': 36.76041941970851}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png', 'icon_background_color': '#FF9E67', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet', 'international_phone_number': '+254 742 894700', 'name': 'Whitefield Restaurant', 'opening_hours': {'open_now': True, 'periods': [{'close': {'day': 0, 'time': '2100'}, 'open': {'day': 0, 'time': '1100'}}, {'close': {'day': 1, 'time': '2100'}, 'open': {'day': 1, 'time': '1100'}}, {'close': {'day': 2, 'time': '2100'}, 'open': {'day': 2, 'time': '1100'}}, {'close': {'day': 3, 'time': '2100'}, 'open': {'day': 3, 'time': '1100'}}, {'close': {'day': 4, 'time': '2100'}, 'open': {'day': 4, 'time': '1100'}}, {'close': {'day': 5, 'time': '2100'}, 'open': {'day': 5, 'time': '1100'}}, {'close': {'day': 6, 'time': '2100'}, 'open': {'day': 6, 'time': '1100'}}], 'weekday_text': ['Monday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Tuesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Wednesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Thursday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Friday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Saturday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Sunday: 11:00\u202fAM\u2009–\u20099:00\u202fPM']}, 'photos': [{'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jkATuC0T8GjDwd36b2qFmdvX05LoynTd7UYt21ecQeWWbhro-dFZ1X5fmPWgnYx3St6-5ceQoznAl9kiFDzRBivsyP_rNHc0jA9vHJ0SZ2wwzamP4FcP2Pu_36nSZObngCkWOcLN3UeLo5meFYAGLaWsxhhiJjlX2QcM64ZL9CP1_bP', 'width': 960}, {'height': 2448, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jnZFX2-uMZTgVBBo52uE6iWjdNFAemLYStnV1LOKq5vrrkdfvLF8UR0VPrYgo9ZzNFPkZusndaGms8EGKdgWpU02jL59Hr-HZy0tgpD13AV1ikVuKAWuxury0aLX5H845y_JoKhcbRhknrAT1tKEpUvnqth6heS34IZvjxEf3YDiXUB', 'width': 3264}, {'height': 4032, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/117873843766263809334">Evans Sigei</a>'], 'photo_reference': 'AUjq9jmoR1PWZKV0rA8iYwS2LqOJJRtntAmFwurFxPNWpm8hQft8wZnDk_RcC-RwLdDv7AxsLTeLrFUNB554gZ2sR1xKR1DJ7DzbjNyGF-aOQh43DMSKMqeCOA4k9Ql99LCTTFzU-fnf6wyCAKq0g1i5QxFgNNBrZGMbIbFFt96A4WGQBO1J', 'width': 3024}, {'height': 1650, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jmJff323BYeFMIzMLzJmxYwD-2g0EDLrOpGks_FbmyrcYfqnstiZ5U5TUNDGNuC0hN0qN0lw8qjnTZCcPmfJvJH5Rw6AnSuVcWACS45D3o9SVDEFFMg1tfSF1uudbSLT54w63lh0QXj4SqOtYxISaUusPahxCXSHqxa-v8-yhVo_t6B', 'width': 1275}, {'height': 3264, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/117685926906985511601">Mahim Hegde</a>'], 'photo_reference': 'AUjq9jnWZfCKYMFcUXoOBWghItru6bc8lwZF7QSaAECOUu-JJ684azbtplyQcjnLdsr_ZA6ocM-G-JaXsjMVKPjen_KKAWKCj2-OfYIRc_rlm0o4sEePGf2NDpwitGMxnQ8itKHweK3L4CeiJx-Mn71j1gbGiVnXPpRHiYfk_4UQYPwJ9o3i', 'width': 2448}, {'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jngXTtuMCD-Pt2OmZcwEKS40hC5rpC9fKJxnx0-ZVLv4RWNt38JRWcaz6xGPXBUKf9sdhH51EhciXmYfM2hWvgi3qNAJvQ6LALvAuP6y3bChqLSefLhlAwQuq395cuhTCoviwWZAjFCO6lsKjDo0mekdGlc4TpxXx2nJUytXq3d1IgS', 'width': 960}, {'height': 1280, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jlNsDNyP6iGDW5G0IEJRTUasz4LkHXbw6YEIly95wgh6fzUSYaAKTL2csQ8n3toTuhUQIsVy6ekD2ZjUXQIk4FHLLkjI_-mIsQWQWmefjh867qtQprVjyC7Cn38OMdbiHq0M1GlEbZNmACByoLF_cr3jgOMZ0bbqSq8P3ySlE15A9J5', 'width': 1280}, {'height': 1280, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jkPG8gKWMtee3Ct8KGUDlber9BW4PqCySq8LhSOYJmAYltKg4hnV-n0UejRM91RHEiW1CCDph049QiJ_wNNowXEX0Ozj0nMjyu0PhF6o01k52bO8BvoViUlSdfOUCom_ZGTw48oMKMvkrCPSGzQuJadfA-DOWbPuiubtO6ur9t-XeYG', 'width': 1280}, {'height': 500, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jn9GgvLFriqvar95wBBO9C44wSkVPpD7BMd6ArKwebr9Lyjq-93XbVEPvkP-pWWnYBfJ6XkLiM21a_W7mNqzv_JlzGnGCUs-YFJ4ugFzmUVWupb-aSM8EdntR7RjNg_hKyGOeXqu_HUOBdTCT7aVgawoy4P9H_i7UN_lps_fmqAJ8ub', 'width': 500}, {'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jlkN2f5c9x01-8wd6hVFQZRITX0Rar1RgnKeViKewap2DNzMoY_5QFqchKpWyqyJrSNd7X2elYUGhA-G-qNoH3cCrNDeexeHV3lMragck_96Kfj4crDmjVqDQNvl-jaE79PhkzmESSV6iOySH8s9lgIyr8o-T27LlqL5z0taUxPvbRq', 'width': 960}], 'place_id': 'ChIJj3S0t1IbLxgRYgL-7uH0NIo', 'plus_code': {'compound_code': 'PQ36+HM Nairobi, Kenya', 'global_code': '6GCRPQ36+HM'}, 'price_level': 2, 'rating': 4.3, 'reference': 'ChIJj3S0t1IbLxgRYgL-7uH0NIo', 'reservable': True, 'reviews': [{'author_name': 'David Kanagaretnam', 'author_url': 'https://www.google.com/maps/contrib/109567623568041706461/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5R7RaF1ueYKm_U0ye8jTBBG7K5T3fjTBWQ1MO4BiQ=s128-c0x00000000-cc-rp-mo-ba5', 'rating': 5, 'relative_time_description': 'a year ago', 'text': 'This is a great restaurant for Indian foods mainly however, you will get Kenyan and others too. A calm place to dine with your family and its has a big parking space.  Staff are welcoming and serving the food fast. The place is clean. Prices for food is affordable.', 'time': 1649416437, 'translated': False}, {'author_name': 'Julliet Esta', 'author_url': 'https://www.google.com/maps/contrib/109510066687005858247/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5TQOlQJn_hcLNSJJbB7omg4O-RCyfpbt-4t3unXQls=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 5, 'relative_time_description': '11 months ago', 'text': "We received a warm welcome, service was fast, the food was great and the portions are definitely enough. I would recommend this restaurant for Indian, Chinese and African cuisine, there's a large parking area, kids play area and also a kids menu. The food was also affordable", 'time': 1651396718, 'translated': False}, {'author_name': 'Aoko Gathoni', 'author_url': 'https://www.google.com/maps/contrib/110036374557197962895/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5RHO3ZIMXY_WihCLk7C2xcQcTKdoc5-QhSNkoWh=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 4, 'relative_time_description': '4 months ago', 'text': "When I arrived, the place looked like it wasn't open. But upon asking someone there, he said it was open.\nI ordered for the half koroga chicken with Naan, and to drink, I had tea masala. I liked that their portions were good size.\nI would definitely go back there.", 'time': 1670771464, 'translated': False}, {'author_name': 'Duncanah Gwat', 'author_url': 'https://www.google.com/maps/contrib/116990714119709426524/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5QXiXwls4KibppDfJxM5IHebKyTFfNr5J2j_LoEmw=s128-c0x00000000-cc-rp-mo-ba2', 'rating': 5, 'relative_time_description': '2 months ago',
        # 'text': 'Beutiful place to be, went for a late lunch, nicely ushered in, the waiter was very polite, super helpful. The serve was quick too. The meal was tasty as well', 'time': 1675536564, 'translated': False}, {'author_name': 'B -', 'author_url': 'https://www.google.com/maps/contrib/111323236689199522335/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5Rp3yfS6xwFBSbA9ZvQjd0F50zh5RkWTANNhk44IeI=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 1, 'relative_time_description': '2 weeks ago', 'text': 'Lovely place. Quiet and clean. Polite and friendly staff and they make really good Indian food. The parking is a bit cramped but overall a good intimate experience. The prices are also very agreeable.\n\nI went back recently and standards have plummeted. Its now a really horrible, depressing restaurant that has no identity. It wants to be an Indian restaurant but cant, also Chinese but not happening. Poor service and food that was definitely not fresh.', 'time': 1680543330, 'translated': False}], 'serves_beer': True, 'serves_brunch': True, 'serves_dinner': True, 'serves_lunch': True, 'serves_vegetarian_food': True, 'serves_wine': True, 'takeout': True, 'types': ['restaurant', 'food', 'point_of_interest', 'establishment'], 'url': 'https://maps.google.com/?cid=9958853927237452386', 'user_ratings_total': 171, 'utc_offset': 180, 'vicinity': 'kingara Road, opp kingara close behind Junction Mall, Nairobi', 'website': 'https://whitefieldrestaurant.reserveport.com/', 'wheelchair_accessible_entrance': True}, 'status': 'OK'}
        return JsonResponse({"data":"All Good"})
    def post(self, request, format=None):
        # place_id_list = request.POST.getlist('place_id_list')
        place_id_list2 = request.POST.get('place_id_list')
        myDict = request.data
        place_id_list = myDict['place_id_list']
        total_succ_queried=list()
        total_failed_queried = list()
        total_succ_saved = list()
        place_id = ''
        result_list = list()
        result_error = list()
        print("raw POSY============")
        print(list(request.POST.items()))
        print("raw rquest============")
        print(place_id_list)
        print(type(place_id_list))
        print("raw rquest2============")
        print(place_id_list2)
        print(type(place_id_list2))
        print("raw simplejspn============")
        print(myDict)
        print(type(myDict))



        try:
            for plc_id in place_id_list:
                place_id = plc_id
                url='https://maps.googleapis.com/maps/api/place/details/json?placeid='+plc_id+'&key=AIzaSyC_oMIdGvpBALKg6W6TPgpwVLb-viGwonY'

                r=requests.get(url)
                results = json.loads(r.text)
                # print("raw results============")
                # print(results)
                resp = retrieve_details(results, plc_id, True)
                if not resp['error']:
                    result_list.append(resp)
                    total_succ_queried.append(plc_id)
                else:
                    result_error.append(resp)
                    total_failed_queried.append(plc_id)

            result_dict = {
                "succesful_results": result_list,
                "failed_results": result_error
            }
            for i in range(len(result_list)):
                re = dh.insert_data(result_list[i])
                if re["isSuccess"]:
                    print("ReqData intserted:  --> insert Id: "+str(re["inserted_id"]))
                    total_succ_saved.append(result_list[i]['place_id'])
                else:
                    error_message = "Could not insert for : "+result_list[i]['place_id']
                    +". Error from server : "+str(re['error'])+"Successful inserted : "
                    +preparing_list_for_error_message(total_succ_saved)+"Succesful queried :"
                    +preparing_list_for_error_message(total_succ_queried)+"Unsucceful queried are : "+preparing_list_for_error_message(total_failed_queried)
                    # error_message = "Could not insert for : "+place_id_list[0]+". Error from server : "+str(True)+"Successful inserted : "+preparing_list_for_error_message(total_succ_saved)+"Succesful queried : "+preparing_list_for_error_message(total_succ_queried)+"Unsuccefull queried : "+preparing_list_for_error_message(total_failed_queried)
                    return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
            return Response(result_dict,status=status.HTTP_200_OK)
        except CustomError:
            return Response("No results for the place id: "+place_id, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("No results for the place id: "+place_id, status=status.HTTP_400_BAD_REQUEST)

class GetPlaceDetailsListStage1(APIView):
    """
    List all countries, or create a new country.
    """
    def get(self, request, format=None):
        # ll = [{"place_id":"EhdQUTM2K0hNLCBOYWlyb2JpLCBLZW55YSImOiQKCg2PPDr_FWtj6RUQChoUChIJp0lN2HIRLxgRTJKXslQCz_c","place_name":"PQ36+HM","category":["street_address"],"address":"PQ36+HM, Nairobi, Kenya","location_coord":"-1.2960625 , 36.7616875","day_hours":"None","phone":"None","website":"None","type_of_data":"scraped","is_test_data":True,"eventId":["FB1010000000000000000000003004"],"error":False}]
        # ll2 = {'html_attributions': [], 'result': {'address_components': [{'long_name': 'Nairobi', 'short_name': 'Nairobi', 'types': ['locality', 'political']}, {'long_name': 'Maziwa', 'short_name': 'Maziwa', 'types': ['sublocality_level_1', 'sublocality', 'political']}, {'long_name': 'Nairobi County', 'short_name': 'Nairobi County', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'Kenya', 'short_name': 'KE', 'types': ['country', 'political']}, {'long_name': '00600', 'short_name': '00600', 'types': ['postal_code']}], 'adr_address': 'kingara Road, <span class="street-address">opp kingara close behind Junction Mall</span>, <span class="postal-code">00600</span>, <span class="locality">Nairobi</span>, <span class="country-name">Kenya</span>', 'business_status': 'OPERATIONAL', 'current_opening_hours': {'open_now': True, 'periods': [{'close': {'date': '2023-04-23', 'day': 0, 'time': '2100'}, 'open': {'date': '2023-04-23', 'day': 0, 'time': '1100'}}, {'close': {'date': '2023-04-24', 'day': 1, 'time': '2100'}, 'open': {'date': '2023-04-24', 'day': 1, 'time': '1100'}}, {'close': {'date': '2023-04-25', 'day': 2, 'time': '2100'}, 'open': {'date': '2023-04-25', 'day': 2, 'time': '1100'}}, {'close': {'date': '2023-04-26', 'day': 3, 'time': '2100'}, 'open': {'date': '2023-04-26', 'day': 3, 'time': '1100'}}, {'close': {'date': '2023-04-27', 'day': 4, 'time': '2100'}, 'open': {'date': '2023-04-27', 'day': 4, 'time': '1100'}}, {'close': {'date': '2023-04-21', 'day': 5, 'time': '2100'}, 'open': {'date': '2023-04-21', 'day': 5, 'time': '1100'}}, {'close': {'date': '2023-04-22', 'day': 6, 'time': '2100'}, 'open': {'date': '2023-04-22', 'day': 6, 'time': '1100'}}], 'weekday_text': ['Monday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Tuesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Wednesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Thursday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Friday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Saturday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Sunday: 11:00\u202fAM\u2009–\u20099:00\u202fPM']}, 'delivery': True, 'dine_in': True, 'formatted_address': 'kingara Road, opp kingara close behind Junction Mall, Nairobi, Kenya', 'formatted_phone_number': '0742 894700', 'geometry': {'location': {'lat': -1.2960063, 'lng': 36.7616708}, 'viewport': {'northeast': {'lat': -1.294604919708498, 'lng': 36.7631173802915}, 'southwest': {'lat': -1.297302880291502, 'lng': 36.76041941970851}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png', 'icon_background_color': '#FF9E67', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet', 'international_phone_number': '+254 742 894700', 'name': 'Whitefield Restaurant', 'opening_hours': {'open_now': True, 'periods': [{'close': {'day': 0, 'time': '2100'}, 'open': {'day': 0, 'time': '1100'}}, {'close': {'day': 1, 'time': '2100'}, 'open': {'day': 1, 'time': '1100'}}, {'close': {'day': 2, 'time': '2100'}, 'open': {'day': 2, 'time': '1100'}}, {'close': {'day': 3, 'time': '2100'}, 'open': {'day': 3, 'time': '1100'}}, {'close': {'day': 4, 'time': '2100'}, 'open': {'day': 4, 'time': '1100'}}, {'close': {'day': 5, 'time': '2100'}, 'open': {'day': 5, 'time': '1100'}}, {'close': {'day': 6, 'time': '2100'}, 'open': {'day': 6, 'time': '1100'}}], 'weekday_text': ['Monday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Tuesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Wednesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Thursday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Friday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Saturday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Sunday: 11:00\u202fAM\u2009–\u20099:00\u202fPM']}, 'photos': [{'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jkATuC0T8GjDwd36b2qFmdvX05LoynTd7UYt21ecQeWWbhro-dFZ1X5fmPWgnYx3St6-5ceQoznAl9kiFDzRBivsyP_rNHc0jA9vHJ0SZ2wwzamP4FcP2Pu_36nSZObngCkWOcLN3UeLo5meFYAGLaWsxhhiJjlX2QcM64ZL9CP1_bP', 'width': 960}, {'height': 2448, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jnZFX2-uMZTgVBBo52uE6iWjdNFAemLYStnV1LOKq5vrrkdfvLF8UR0VPrYgo9ZzNFPkZusndaGms8EGKdgWpU02jL59Hr-HZy0tgpD13AV1ikVuKAWuxury0aLX5H845y_JoKhcbRhknrAT1tKEpUvnqth6heS34IZvjxEf3YDiXUB', 'width': 3264}, {'height': 4032, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/117873843766263809334">Evans Sigei</a>'], 'photo_reference': 'AUjq9jmoR1PWZKV0rA8iYwS2LqOJJRtntAmFwurFxPNWpm8hQft8wZnDk_RcC-RwLdDv7AxsLTeLrFUNB554gZ2sR1xKR1DJ7DzbjNyGF-aOQh43DMSKMqeCOA4k9Ql99LCTTFzU-fnf6wyCAKq0g1i5QxFgNNBrZGMbIbFFt96A4WGQBO1J', 'width': 3024}, {'height': 1650, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jmJff323BYeFMIzMLzJmxYwD-2g0EDLrOpGks_FbmyrcYfqnstiZ5U5TUNDGNuC0hN0qN0lw8qjnTZCcPmfJvJH5Rw6AnSuVcWACS45D3o9SVDEFFMg1tfSF1uudbSLT54w63lh0QXj4SqOtYxISaUusPahxCXSHqxa-v8-yhVo_t6B', 'width': 1275}, {'height': 3264, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/117685926906985511601">Mahim Hegde</a>'], 'photo_reference': 'AUjq9jnWZfCKYMFcUXoOBWghItru6bc8lwZF7QSaAECOUu-JJ684azbtplyQcjnLdsr_ZA6ocM-G-JaXsjMVKPjen_KKAWKCj2-OfYIRc_rlm0o4sEePGf2NDpwitGMxnQ8itKHweK3L4CeiJx-Mn71j1gbGiVnXPpRHiYfk_4UQYPwJ9o3i', 'width': 2448}, {'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jngXTtuMCD-Pt2OmZcwEKS40hC5rpC9fKJxnx0-ZVLv4RWNt38JRWcaz6xGPXBUKf9sdhH51EhciXmYfM2hWvgi3qNAJvQ6LALvAuP6y3bChqLSefLhlAwQuq395cuhTCoviwWZAjFCO6lsKjDo0mekdGlc4TpxXx2nJUytXq3d1IgS', 'width': 960}, {'height': 1280, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jlNsDNyP6iGDW5G0IEJRTUasz4LkHXbw6YEIly95wgh6fzUSYaAKTL2csQ8n3toTuhUQIsVy6ekD2ZjUXQIk4FHLLkjI_-mIsQWQWmefjh867qtQprVjyC7Cn38OMdbiHq0M1GlEbZNmACByoLF_cr3jgOMZ0bbqSq8P3ySlE15A9J5', 'width': 1280}, {'height': 1280, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jkPG8gKWMtee3Ct8KGUDlber9BW4PqCySq8LhSOYJmAYltKg4hnV-n0UejRM91RHEiW1CCDph049QiJ_wNNowXEX0Ozj0nMjyu0PhF6o01k52bO8BvoViUlSdfOUCom_ZGTw48oMKMvkrCPSGzQuJadfA-DOWbPuiubtO6ur9t-XeYG', 'width': 1280}, {'height': 500, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jn9GgvLFriqvar95wBBO9C44wSkVPpD7BMd6ArKwebr9Lyjq-93XbVEPvkP-pWWnYBfJ6XkLiM21a_W7mNqzv_JlzGnGCUs-YFJ4ugFzmUVWupb-aSM8EdntR7RjNg_hKyGOeXqu_HUOBdTCT7aVgawoy4P9H_i7UN_lps_fmqAJ8ub', 'width': 500}, {'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jlkN2f5c9x01-8wd6hVFQZRITX0Rar1RgnKeViKewap2DNzMoY_5QFqchKpWyqyJrSNd7X2elYUGhA-G-qNoH3cCrNDeexeHV3lMragck_96Kfj4crDmjVqDQNvl-jaE79PhkzmESSV6iOySH8s9lgIyr8o-T27LlqL5z0taUxPvbRq', 'width': 960}], 'place_id': 'ChIJj3S0t1IbLxgRYgL-7uH0NIo', 'plus_code': {'compound_code': 'PQ36+HM Nairobi, Kenya', 'global_code': '6GCRPQ36+HM'}, 'price_level': 2, 'rating': 4.3, 'reference': 'ChIJj3S0t1IbLxgRYgL-7uH0NIo', 'reservable': True, 'reviews': [{'author_name': 'David Kanagaretnam', 'author_url': 'https://www.google.com/maps/contrib/109567623568041706461/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5R7RaF1ueYKm_U0ye8jTBBG7K5T3fjTBWQ1MO4BiQ=s128-c0x00000000-cc-rp-mo-ba5', 'rating': 5, 'relative_time_description': 'a year ago', 'text': 'This is a great restaurant for Indian foods mainly however, you will get Kenyan and others too. A calm place to dine with your family and its has a big parking space.  Staff are welcoming and serving the food fast. The place is clean. Prices for food is affordable.', 'time': 1649416437, 'translated': False}, {'author_name': 'Julliet Esta', 'author_url': 'https://www.google.com/maps/contrib/109510066687005858247/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5TQOlQJn_hcLNSJJbB7omg4O-RCyfpbt-4t3unXQls=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 5, 'relative_time_description': '11 months ago', 'text': "We received a warm welcome, service was fast, the food was great and the portions are definitely enough. I would recommend this restaurant for Indian, Chinese and African cuisine, there's a large parking area, kids play area and also a kids menu. The food was also affordable", 'time': 1651396718, 'translated': False}, {'author_name': 'Aoko Gathoni', 'author_url': 'https://www.google.com/maps/contrib/110036374557197962895/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5RHO3ZIMXY_WihCLk7C2xcQcTKdoc5-QhSNkoWh=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 4, 'relative_time_description': '4 months ago', 'text': "When I arrived, the place looked like it wasn't open. But upon asking someone there, he said it was open.\nI ordered for the half koroga chicken with Naan, and to drink, I had tea masala. I liked that their portions were good size.\nI would definitely go back there.", 'time': 1670771464, 'translated': False}, {'author_name': 'Duncanah Gwat', 'author_url': 'https://www.google.com/maps/contrib/116990714119709426524/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5QXiXwls4KibppDfJxM5IHebKyTFfNr5J2j_LoEmw=s128-c0x00000000-cc-rp-mo-ba2', 'rating': 5, 'relative_time_description': '2 months ago',
        # 'text': 'Beutiful place to be, went for a late lunch, nicely ushered in, the waiter was very polite, super helpful. The serve was quick too. The meal was tasty as well', 'time': 1675536564, 'translated': False}, {'author_name': 'B -', 'author_url': 'https://www.google.com/maps/contrib/111323236689199522335/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5Rp3yfS6xwFBSbA9ZvQjd0F50zh5RkWTANNhk44IeI=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 1, 'relative_time_description': '2 weeks ago', 'text': 'Lovely place. Quiet and clean. Polite and friendly staff and they make really good Indian food. The parking is a bit cramped but overall a good intimate experience. The prices are also very agreeable.\n\nI went back recently and standards have plummeted. Its now a really horrible, depressing restaurant that has no identity. It wants to be an Indian restaurant but cant, also Chinese but not happening. Poor service and food that was definitely not fresh.', 'time': 1680543330, 'translated': False}], 'serves_beer': True, 'serves_brunch': True, 'serves_dinner': True, 'serves_lunch': True, 'serves_vegetarian_food': True, 'serves_wine': True, 'takeout': True, 'types': ['restaurant', 'food', 'point_of_interest', 'establishment'], 'url': 'https://maps.google.com/?cid=9958853927237452386', 'user_ratings_total': 171, 'utc_offset': 180, 'vicinity': 'kingara Road, opp kingara close behind Junction Mall, Nairobi', 'website': 'https://whitefieldrestaurant.reserveport.com/', 'wheelchair_accessible_entrance': True}, 'status': 'OK'}
        return JsonResponse({"data":"All Good"})
    def post(self, request, format=None):
        # place_id_list = request.POST.getlist('place_id_list')
        place_id_list2 = request.POST.get('place_id_list')
        myDict = request.data
        place_id_list = myDict['place_id_list']
        total_succ_queried=list()
        total_failed_queried = list()
        total_succ_saved = list()
        place_id = ''
        result_list = list()
        result_error = list()
        print("raw POSY============")
        print(list(request.POST.items()))
        print("raw rquest============")
        print(place_id_list)
        print(type(place_id_list))
        print("raw rquest2============")
        print(place_id_list2)
        print(type(place_id_list2))
        print("raw simplejspn============")
        print(myDict)
        print(type(myDict))



        try:
            for plc_id in place_id_list:
                place_id = plc_id
                url='https://maps.googleapis.com/maps/api/place/details/json?placeid='+plc_id+'&key=AIzaSyC_oMIdGvpBALKg6W6TPgpwVLb-viGwonY'

                r=requests.get(url)
                results = json.loads(r.text)
                # print("raw results============")
                # print(results)
                resp = retrieve_details(results, plc_id, True)
                if not resp['error']:
                    result_list.append(resp)
                    total_succ_queried.append(plc_id)
                else:
                    result_error.append(resp)
                    total_failed_queried.append(plc_id)

            result_dict = {
                "succesful_results": result_list,
                "failed_results": result_error
            }
            return Response(result_dict,status=status.HTTP_200_OK)
        except CustomError:
            return Response("No results for the place id: "+place_id, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("No results for the place id: "+place_id, status=status.HTTP_400_BAD_REQUEST)



class GetPlaceDetailsListStage2(APIView):
    """
    List all countries, or create a new country.
    """
    def get(self, request, format=None):
        # ll = [{"place_id":"EhdQUTM2K0hNLCBOYWlyb2JpLCBLZW55YSImOiQKCg2PPDr_FWtj6RUQChoUChIJp0lN2HIRLxgRTJKXslQCz_c","place_name":"PQ36+HM","category":["street_address"],"address":"PQ36+HM, Nairobi, Kenya","location_coord":"-1.2960625 , 36.7616875","day_hours":"None","phone":"None","website":"None","type_of_data":"scraped","is_test_data":True,"eventId":["FB1010000000000000000000003004"],"error":False}]
        # ll2 = {'html_attributions': [], 'result': {'address_components': [{'long_name': 'Nairobi', 'short_name': 'Nairobi', 'types': ['locality', 'political']}, {'long_name': 'Maziwa', 'short_name': 'Maziwa', 'types': ['sublocality_level_1', 'sublocality', 'political']}, {'long_name': 'Nairobi County', 'short_name': 'Nairobi County', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'Kenya', 'short_name': 'KE', 'types': ['country', 'political']}, {'long_name': '00600', 'short_name': '00600', 'types': ['postal_code']}], 'adr_address': 'kingara Road, <span class="street-address">opp kingara close behind Junction Mall</span>, <span class="postal-code">00600</span>, <span class="locality">Nairobi</span>, <span class="country-name">Kenya</span>', 'business_status': 'OPERATIONAL', 'current_opening_hours': {'open_now': True, 'periods': [{'close': {'date': '2023-04-23', 'day': 0, 'time': '2100'}, 'open': {'date': '2023-04-23', 'day': 0, 'time': '1100'}}, {'close': {'date': '2023-04-24', 'day': 1, 'time': '2100'}, 'open': {'date': '2023-04-24', 'day': 1, 'time': '1100'}}, {'close': {'date': '2023-04-25', 'day': 2, 'time': '2100'}, 'open': {'date': '2023-04-25', 'day': 2, 'time': '1100'}}, {'close': {'date': '2023-04-26', 'day': 3, 'time': '2100'}, 'open': {'date': '2023-04-26', 'day': 3, 'time': '1100'}}, {'close': {'date': '2023-04-27', 'day': 4, 'time': '2100'}, 'open': {'date': '2023-04-27', 'day': 4, 'time': '1100'}}, {'close': {'date': '2023-04-21', 'day': 5, 'time': '2100'}, 'open': {'date': '2023-04-21', 'day': 5, 'time': '1100'}}, {'close': {'date': '2023-04-22', 'day': 6, 'time': '2100'}, 'open': {'date': '2023-04-22', 'day': 6, 'time': '1100'}}], 'weekday_text': ['Monday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Tuesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Wednesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Thursday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Friday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Saturday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Sunday: 11:00\u202fAM\u2009–\u20099:00\u202fPM']}, 'delivery': True, 'dine_in': True, 'formatted_address': 'kingara Road, opp kingara close behind Junction Mall, Nairobi, Kenya', 'formatted_phone_number': '0742 894700', 'geometry': {'location': {'lat': -1.2960063, 'lng': 36.7616708}, 'viewport': {'northeast': {'lat': -1.294604919708498, 'lng': 36.7631173802915}, 'southwest': {'lat': -1.297302880291502, 'lng': 36.76041941970851}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png', 'icon_background_color': '#FF9E67', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet', 'international_phone_number': '+254 742 894700', 'name': 'Whitefield Restaurant', 'opening_hours': {'open_now': True, 'periods': [{'close': {'day': 0, 'time': '2100'}, 'open': {'day': 0, 'time': '1100'}}, {'close': {'day': 1, 'time': '2100'}, 'open': {'day': 1, 'time': '1100'}}, {'close': {'day': 2, 'time': '2100'}, 'open': {'day': 2, 'time': '1100'}}, {'close': {'day': 3, 'time': '2100'}, 'open': {'day': 3, 'time': '1100'}}, {'close': {'day': 4, 'time': '2100'}, 'open': {'day': 4, 'time': '1100'}}, {'close': {'day': 5, 'time': '2100'}, 'open': {'day': 5, 'time': '1100'}}, {'close': {'day': 6, 'time': '2100'}, 'open': {'day': 6, 'time': '1100'}}], 'weekday_text': ['Monday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Tuesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Wednesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Thursday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Friday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Saturday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Sunday: 11:00\u202fAM\u2009–\u20099:00\u202fPM']}, 'photos': [{'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jkATuC0T8GjDwd36b2qFmdvX05LoynTd7UYt21ecQeWWbhro-dFZ1X5fmPWgnYx3St6-5ceQoznAl9kiFDzRBivsyP_rNHc0jA9vHJ0SZ2wwzamP4FcP2Pu_36nSZObngCkWOcLN3UeLo5meFYAGLaWsxhhiJjlX2QcM64ZL9CP1_bP', 'width': 960}, {'height': 2448, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jnZFX2-uMZTgVBBo52uE6iWjdNFAemLYStnV1LOKq5vrrkdfvLF8UR0VPrYgo9ZzNFPkZusndaGms8EGKdgWpU02jL59Hr-HZy0tgpD13AV1ikVuKAWuxury0aLX5H845y_JoKhcbRhknrAT1tKEpUvnqth6heS34IZvjxEf3YDiXUB', 'width': 3264}, {'height': 4032, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/117873843766263809334">Evans Sigei</a>'], 'photo_reference': 'AUjq9jmoR1PWZKV0rA8iYwS2LqOJJRtntAmFwurFxPNWpm8hQft8wZnDk_RcC-RwLdDv7AxsLTeLrFUNB554gZ2sR1xKR1DJ7DzbjNyGF-aOQh43DMSKMqeCOA4k9Ql99LCTTFzU-fnf6wyCAKq0g1i5QxFgNNBrZGMbIbFFt96A4WGQBO1J', 'width': 3024}, {'height': 1650, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jmJff323BYeFMIzMLzJmxYwD-2g0EDLrOpGks_FbmyrcYfqnstiZ5U5TUNDGNuC0hN0qN0lw8qjnTZCcPmfJvJH5Rw6AnSuVcWACS45D3o9SVDEFFMg1tfSF1uudbSLT54w63lh0QXj4SqOtYxISaUusPahxCXSHqxa-v8-yhVo_t6B', 'width': 1275}, {'height': 3264, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/117685926906985511601">Mahim Hegde</a>'], 'photo_reference': 'AUjq9jnWZfCKYMFcUXoOBWghItru6bc8lwZF7QSaAECOUu-JJ684azbtplyQcjnLdsr_ZA6ocM-G-JaXsjMVKPjen_KKAWKCj2-OfYIRc_rlm0o4sEePGf2NDpwitGMxnQ8itKHweK3L4CeiJx-Mn71j1gbGiVnXPpRHiYfk_4UQYPwJ9o3i', 'width': 2448}, {'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jngXTtuMCD-Pt2OmZcwEKS40hC5rpC9fKJxnx0-ZVLv4RWNt38JRWcaz6xGPXBUKf9sdhH51EhciXmYfM2hWvgi3qNAJvQ6LALvAuP6y3bChqLSefLhlAwQuq395cuhTCoviwWZAjFCO6lsKjDo0mekdGlc4TpxXx2nJUytXq3d1IgS', 'width': 960}, {'height': 1280, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jlNsDNyP6iGDW5G0IEJRTUasz4LkHXbw6YEIly95wgh6fzUSYaAKTL2csQ8n3toTuhUQIsVy6ekD2ZjUXQIk4FHLLkjI_-mIsQWQWmefjh867qtQprVjyC7Cn38OMdbiHq0M1GlEbZNmACByoLF_cr3jgOMZ0bbqSq8P3ySlE15A9J5', 'width': 1280}, {'height': 1280, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jkPG8gKWMtee3Ct8KGUDlber9BW4PqCySq8LhSOYJmAYltKg4hnV-n0UejRM91RHEiW1CCDph049QiJ_wNNowXEX0Ozj0nMjyu0PhF6o01k52bO8BvoViUlSdfOUCom_ZGTw48oMKMvkrCPSGzQuJadfA-DOWbPuiubtO6ur9t-XeYG', 'width': 1280}, {'height': 500, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jn9GgvLFriqvar95wBBO9C44wSkVPpD7BMd6ArKwebr9Lyjq-93XbVEPvkP-pWWnYBfJ6XkLiM21a_W7mNqzv_JlzGnGCUs-YFJ4ugFzmUVWupb-aSM8EdntR7RjNg_hKyGOeXqu_HUOBdTCT7aVgawoy4P9H_i7UN_lps_fmqAJ8ub', 'width': 500}, {'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jlkN2f5c9x01-8wd6hVFQZRITX0Rar1RgnKeViKewap2DNzMoY_5QFqchKpWyqyJrSNd7X2elYUGhA-G-qNoH3cCrNDeexeHV3lMragck_96Kfj4crDmjVqDQNvl-jaE79PhkzmESSV6iOySH8s9lgIyr8o-T27LlqL5z0taUxPvbRq', 'width': 960}], 'place_id': 'ChIJj3S0t1IbLxgRYgL-7uH0NIo', 'plus_code': {'compound_code': 'PQ36+HM Nairobi, Kenya', 'global_code': '6GCRPQ36+HM'}, 'price_level': 2, 'rating': 4.3, 'reference': 'ChIJj3S0t1IbLxgRYgL-7uH0NIo', 'reservable': True, 'reviews': [{'author_name': 'David Kanagaretnam', 'author_url': 'https://www.google.com/maps/contrib/109567623568041706461/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5R7RaF1ueYKm_U0ye8jTBBG7K5T3fjTBWQ1MO4BiQ=s128-c0x00000000-cc-rp-mo-ba5', 'rating': 5, 'relative_time_description': 'a year ago', 'text': 'This is a great restaurant for Indian foods mainly however, you will get Kenyan and others too. A calm place to dine with your family and its has a big parking space.  Staff are welcoming and serving the food fast. The place is clean. Prices for food is affordable.', 'time': 1649416437, 'translated': False}, {'author_name': 'Julliet Esta', 'author_url': 'https://www.google.com/maps/contrib/109510066687005858247/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5TQOlQJn_hcLNSJJbB7omg4O-RCyfpbt-4t3unXQls=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 5, 'relative_time_description': '11 months ago', 'text': "We received a warm welcome, service was fast, the food was great and the portions are definitely enough. I would recommend this restaurant for Indian, Chinese and African cuisine, there's a large parking area, kids play area and also a kids menu. The food was also affordable", 'time': 1651396718, 'translated': False}, {'author_name': 'Aoko Gathoni', 'author_url': 'https://www.google.com/maps/contrib/110036374557197962895/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5RHO3ZIMXY_WihCLk7C2xcQcTKdoc5-QhSNkoWh=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 4, 'relative_time_description': '4 months ago', 'text': "When I arrived, the place looked like it wasn't open. But upon asking someone there, he said it was open.\nI ordered for the half koroga chicken with Naan, and to drink, I had tea masala. I liked that their portions were good size.\nI would definitely go back there.", 'time': 1670771464, 'translated': False}, {'author_name': 'Duncanah Gwat', 'author_url': 'https://www.google.com/maps/contrib/116990714119709426524/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5QXiXwls4KibppDfJxM5IHebKyTFfNr5J2j_LoEmw=s128-c0x00000000-cc-rp-mo-ba2', 'rating': 5, 'relative_time_description': '2 months ago',
        # 'text': 'Beutiful place to be, went for a late lunch, nicely ushered in, the waiter was very polite, super helpful. The serve was quick too. The meal was tasty as well', 'time': 1675536564, 'translated': False}, {'author_name': 'B -', 'author_url': 'https://www.google.com/maps/contrib/111323236689199522335/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5Rp3yfS6xwFBSbA9ZvQjd0F50zh5RkWTANNhk44IeI=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 1, 'relative_time_description': '2 weeks ago', 'text': 'Lovely place. Quiet and clean. Polite and friendly staff and they make really good Indian food. The parking is a bit cramped but overall a good intimate experience. The prices are also very agreeable.\n\nI went back recently and standards have plummeted. Its now a really horrible, depressing restaurant that has no identity. It wants to be an Indian restaurant but cant, also Chinese but not happening. Poor service and food that was definitely not fresh.', 'time': 1680543330, 'translated': False}], 'serves_beer': True, 'serves_brunch': True, 'serves_dinner': True, 'serves_lunch': True, 'serves_vegetarian_food': True, 'serves_wine': True, 'takeout': True, 'types': ['restaurant', 'food', 'point_of_interest', 'establishment'], 'url': 'https://maps.google.com/?cid=9958853927237452386', 'user_ratings_total': 171, 'utc_offset': 180, 'vicinity': 'kingara Road, opp kingara close behind Junction Mall, Nairobi', 'website': 'https://whitefieldrestaurant.reserveport.com/', 'wheelchair_accessible_entrance': True}, 'status': 'OK'}
        return JsonResponse({"data":"All Good"})
    def post(self, request, format=None):
        # place_id_list = request.POST.getlist('place_id_list')
        # result_dict = request.POST.get('result_dict')
        myDict = request.data
        result_dict = myDict['result_dict']
        total_succ_queried=list()
        total_failed_queried = list()
        total_succ_saved = list()
        place_id = ''
        result_list = result_dict['succesful_results']
        result_error = list()
        print("raw POSY============")
        print(list(request.POST.items()))
        print(myDict)
        print(type(myDict))



        try:
            success_mess = "Saved Succesfully"
            for i in range(len(result_list)):
                re = dh.insert_data(result_list[i])
                if re["isSuccess"]:
                    print("ReqData intserted:  --> insert Id: "+str(re["inserted_id"]))
                    total_succ_saved.append(result_list[i]['place_id'])
                else:
                    error_message = "Could not insert for : "+result_list[i]['place_id']
                    +". Error from server : "+str(re['error'])+"Successful inserted : "
                    +preparing_list_for_error_message(total_succ_saved)+"Succesful queried :"
                    +preparing_list_for_error_message(total_succ_queried)+"Unsucceful queried are : "+preparing_list_for_error_message(total_failed_queried)
                    # error_message = "Could not insert for : "+place_id_list[0]+". Error from server : "+str(True)+"Successful inserted : "+preparing_list_for_error_message(total_succ_saved)+"Succesful queried : "+preparing_list_for_error_message(total_succ_queried)+"Unsuccefull queried : "+preparing_list_for_error_message(total_failed_queried)
                    return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
            return Response(success_mess,status=status.HTTP_200_OK)
        except CustomError:
            return Response("No results for the place id: "+place_id, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("No results for the place id: "+place_id, status=status.HTTP_400_BAD_REQUEST)

class VerifyPlaceIds(APIView):
    """
    List all countries, or create a new country.
    """
    def get(self, request, format=None):
        # ll = [{"place_id":"EhdQUTM2K0hNLCBOYWlyb2JpLCBLZW55YSImOiQKCg2PPDr_FWtj6RUQChoUChIJp0lN2HIRLxgRTJKXslQCz_c","place_name":"PQ36+HM","category":["street_address"],"address":"PQ36+HM, Nairobi, Kenya","location_coord":"-1.2960625 , 36.7616875","day_hours":"None","phone":"None","website":"None","type_of_data":"scraped","is_test_data":True,"eventId":["FB1010000000000000000000003004"],"error":False}]
        # ll2 = {'html_attributions': [], 'result': {'address_components': [{'long_name': 'Nairobi', 'short_name': 'Nairobi', 'types': ['locality', 'political']}, {'long_name': 'Maziwa', 'short_name': 'Maziwa', 'types': ['sublocality_level_1', 'sublocality', 'political']}, {'long_name': 'Nairobi County', 'short_name': 'Nairobi County', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'Kenya', 'short_name': 'KE', 'types': ['country', 'political']}, {'long_name': '00600', 'short_name': '00600', 'types': ['postal_code']}], 'adr_address': 'kingara Road, <span class="street-address">opp kingara close behind Junction Mall</span>, <span class="postal-code">00600</span>, <span class="locality">Nairobi</span>, <span class="country-name">Kenya</span>', 'business_status': 'OPERATIONAL', 'current_opening_hours': {'open_now': True, 'periods': [{'close': {'date': '2023-04-23', 'day': 0, 'time': '2100'}, 'open': {'date': '2023-04-23', 'day': 0, 'time': '1100'}}, {'close': {'date': '2023-04-24', 'day': 1, 'time': '2100'}, 'open': {'date': '2023-04-24', 'day': 1, 'time': '1100'}}, {'close': {'date': '2023-04-25', 'day': 2, 'time': '2100'}, 'open': {'date': '2023-04-25', 'day': 2, 'time': '1100'}}, {'close': {'date': '2023-04-26', 'day': 3, 'time': '2100'}, 'open': {'date': '2023-04-26', 'day': 3, 'time': '1100'}}, {'close': {'date': '2023-04-27', 'day': 4, 'time': '2100'}, 'open': {'date': '2023-04-27', 'day': 4, 'time': '1100'}}, {'close': {'date': '2023-04-21', 'day': 5, 'time': '2100'}, 'open': {'date': '2023-04-21', 'day': 5, 'time': '1100'}}, {'close': {'date': '2023-04-22', 'day': 6, 'time': '2100'}, 'open': {'date': '2023-04-22', 'day': 6, 'time': '1100'}}], 'weekday_text': ['Monday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Tuesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Wednesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Thursday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Friday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Saturday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Sunday: 11:00\u202fAM\u2009–\u20099:00\u202fPM']}, 'delivery': True, 'dine_in': True, 'formatted_address': 'kingara Road, opp kingara close behind Junction Mall, Nairobi, Kenya', 'formatted_phone_number': '0742 894700', 'geometry': {'location': {'lat': -1.2960063, 'lng': 36.7616708}, 'viewport': {'northeast': {'lat': -1.294604919708498, 'lng': 36.7631173802915}, 'southwest': {'lat': -1.297302880291502, 'lng': 36.76041941970851}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png', 'icon_background_color': '#FF9E67', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet', 'international_phone_number': '+254 742 894700', 'name': 'Whitefield Restaurant', 'opening_hours': {'open_now': True, 'periods': [{'close': {'day': 0, 'time': '2100'}, 'open': {'day': 0, 'time': '1100'}}, {'close': {'day': 1, 'time': '2100'}, 'open': {'day': 1, 'time': '1100'}}, {'close': {'day': 2, 'time': '2100'}, 'open': {'day': 2, 'time': '1100'}}, {'close': {'day': 3, 'time': '2100'}, 'open': {'day': 3, 'time': '1100'}}, {'close': {'day': 4, 'time': '2100'}, 'open': {'day': 4, 'time': '1100'}}, {'close': {'day': 5, 'time': '2100'}, 'open': {'day': 5, 'time': '1100'}}, {'close': {'day': 6, 'time': '2100'}, 'open': {'day': 6, 'time': '1100'}}], 'weekday_text': ['Monday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Tuesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Wednesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Thursday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Friday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Saturday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Sunday: 11:00\u202fAM\u2009–\u20099:00\u202fPM']}, 'photos': [{'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jkATuC0T8GjDwd36b2qFmdvX05LoynTd7UYt21ecQeWWbhro-dFZ1X5fmPWgnYx3St6-5ceQoznAl9kiFDzRBivsyP_rNHc0jA9vHJ0SZ2wwzamP4FcP2Pu_36nSZObngCkWOcLN3UeLo5meFYAGLaWsxhhiJjlX2QcM64ZL9CP1_bP', 'width': 960}, {'height': 2448, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jnZFX2-uMZTgVBBo52uE6iWjdNFAemLYStnV1LOKq5vrrkdfvLF8UR0VPrYgo9ZzNFPkZusndaGms8EGKdgWpU02jL59Hr-HZy0tgpD13AV1ikVuKAWuxury0aLX5H845y_JoKhcbRhknrAT1tKEpUvnqth6heS34IZvjxEf3YDiXUB', 'width': 3264}, {'height': 4032, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/117873843766263809334">Evans Sigei</a>'], 'photo_reference': 'AUjq9jmoR1PWZKV0rA8iYwS2LqOJJRtntAmFwurFxPNWpm8hQft8wZnDk_RcC-RwLdDv7AxsLTeLrFUNB554gZ2sR1xKR1DJ7DzbjNyGF-aOQh43DMSKMqeCOA4k9Ql99LCTTFzU-fnf6wyCAKq0g1i5QxFgNNBrZGMbIbFFt96A4WGQBO1J', 'width': 3024}, {'height': 1650, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jmJff323BYeFMIzMLzJmxYwD-2g0EDLrOpGks_FbmyrcYfqnstiZ5U5TUNDGNuC0hN0qN0lw8qjnTZCcPmfJvJH5Rw6AnSuVcWACS45D3o9SVDEFFMg1tfSF1uudbSLT54w63lh0QXj4SqOtYxISaUusPahxCXSHqxa-v8-yhVo_t6B', 'width': 1275}, {'height': 3264, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/117685926906985511601">Mahim Hegde</a>'], 'photo_reference': 'AUjq9jnWZfCKYMFcUXoOBWghItru6bc8lwZF7QSaAECOUu-JJ684azbtplyQcjnLdsr_ZA6ocM-G-JaXsjMVKPjen_KKAWKCj2-OfYIRc_rlm0o4sEePGf2NDpwitGMxnQ8itKHweK3L4CeiJx-Mn71j1gbGiVnXPpRHiYfk_4UQYPwJ9o3i', 'width': 2448}, {'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jngXTtuMCD-Pt2OmZcwEKS40hC5rpC9fKJxnx0-ZVLv4RWNt38JRWcaz6xGPXBUKf9sdhH51EhciXmYfM2hWvgi3qNAJvQ6LALvAuP6y3bChqLSefLhlAwQuq395cuhTCoviwWZAjFCO6lsKjDo0mekdGlc4TpxXx2nJUytXq3d1IgS', 'width': 960}, {'height': 1280, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jlNsDNyP6iGDW5G0IEJRTUasz4LkHXbw6YEIly95wgh6fzUSYaAKTL2csQ8n3toTuhUQIsVy6ekD2ZjUXQIk4FHLLkjI_-mIsQWQWmefjh867qtQprVjyC7Cn38OMdbiHq0M1GlEbZNmACByoLF_cr3jgOMZ0bbqSq8P3ySlE15A9J5', 'width': 1280}, {'height': 1280, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jkPG8gKWMtee3Ct8KGUDlber9BW4PqCySq8LhSOYJmAYltKg4hnV-n0UejRM91RHEiW1CCDph049QiJ_wNNowXEX0Ozj0nMjyu0PhF6o01k52bO8BvoViUlSdfOUCom_ZGTw48oMKMvkrCPSGzQuJadfA-DOWbPuiubtO6ur9t-XeYG', 'width': 1280}, {'height': 500, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jn9GgvLFriqvar95wBBO9C44wSkVPpD7BMd6ArKwebr9Lyjq-93XbVEPvkP-pWWnYBfJ6XkLiM21a_W7mNqzv_JlzGnGCUs-YFJ4ugFzmUVWupb-aSM8EdntR7RjNg_hKyGOeXqu_HUOBdTCT7aVgawoy4P9H_i7UN_lps_fmqAJ8ub', 'width': 500}, {'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jlkN2f5c9x01-8wd6hVFQZRITX0Rar1RgnKeViKewap2DNzMoY_5QFqchKpWyqyJrSNd7X2elYUGhA-G-qNoH3cCrNDeexeHV3lMragck_96Kfj4crDmjVqDQNvl-jaE79PhkzmESSV6iOySH8s9lgIyr8o-T27LlqL5z0taUxPvbRq', 'width': 960}], 'place_id': 'ChIJj3S0t1IbLxgRYgL-7uH0NIo', 'plus_code': {'compound_code': 'PQ36+HM Nairobi, Kenya', 'global_code': '6GCRPQ36+HM'}, 'price_level': 2, 'rating': 4.3, 'reference': 'ChIJj3S0t1IbLxgRYgL-7uH0NIo', 'reservable': True, 'reviews': [{'author_name': 'David Kanagaretnam', 'author_url': 'https://www.google.com/maps/contrib/109567623568041706461/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5R7RaF1ueYKm_U0ye8jTBBG7K5T3fjTBWQ1MO4BiQ=s128-c0x00000000-cc-rp-mo-ba5', 'rating': 5, 'relative_time_description': 'a year ago', 'text': 'This is a great restaurant for Indian foods mainly however, you will get Kenyan and others too. A calm place to dine with your family and its has a big parking space.  Staff are welcoming and serving the food fast. The place is clean. Prices for food is affordable.', 'time': 1649416437, 'translated': False}, {'author_name': 'Julliet Esta', 'author_url': 'https://www.google.com/maps/contrib/109510066687005858247/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5TQOlQJn_hcLNSJJbB7omg4O-RCyfpbt-4t3unXQls=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 5, 'relative_time_description': '11 months ago', 'text': "We received a warm welcome, service was fast, the food was great and the portions are definitely enough. I would recommend this restaurant for Indian, Chinese and African cuisine, there's a large parking area, kids play area and also a kids menu. The food was also affordable", 'time': 1651396718, 'translated': False}, {'author_name': 'Aoko Gathoni', 'author_url': 'https://www.google.com/maps/contrib/110036374557197962895/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5RHO3ZIMXY_WihCLk7C2xcQcTKdoc5-QhSNkoWh=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 4, 'relative_time_description': '4 months ago', 'text': "When I arrived, the place looked like it wasn't open. But upon asking someone there, he said it was open.\nI ordered for the half koroga chicken with Naan, and to drink, I had tea masala. I liked that their portions were good size.\nI would definitely go back there.", 'time': 1670771464, 'translated': False}, {'author_name': 'Duncanah Gwat', 'author_url': 'https://www.google.com/maps/contrib/116990714119709426524/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5QXiXwls4KibppDfJxM5IHebKyTFfNr5J2j_LoEmw=s128-c0x00000000-cc-rp-mo-ba2', 'rating': 5, 'relative_time_description': '2 months ago',
        # 'text': 'Beutiful place to be, went for a late lunch, nicely ushered in, the waiter was very polite, super helpful. The serve was quick too. The meal was tasty as well', 'time': 1675536564, 'translated': False}, {'author_name': 'B -', 'author_url': 'https://www.google.com/maps/contrib/111323236689199522335/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5Rp3yfS6xwFBSbA9ZvQjd0F50zh5RkWTANNhk44IeI=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 1, 'relative_time_description': '2 weeks ago', 'text': 'Lovely place. Quiet and clean. Polite and friendly staff and they make really good Indian food. The parking is a bit cramped but overall a good intimate experience. The prices are also very agreeable.\n\nI went back recently and standards have plummeted. Its now a really horrible, depressing restaurant that has no identity. It wants to be an Indian restaurant but cant, also Chinese but not happening. Poor service and food that was definitely not fresh.', 'time': 1680543330, 'translated': False}], 'serves_beer': True, 'serves_brunch': True, 'serves_dinner': True, 'serves_lunch': True, 'serves_vegetarian_food': True, 'serves_wine': True, 'takeout': True, 'types': ['restaurant', 'food', 'point_of_interest', 'establishment'], 'url': 'https://maps.google.com/?cid=9958853927237452386', 'user_ratings_total': 171, 'utc_offset': 180, 'vicinity': 'kingara Road, opp kingara close behind Junction Mall, Nairobi', 'website': 'https://whitefieldrestaurant.reserveport.com/', 'wheelchair_accessible_entrance': True}, 'status': 'OK'}
        return JsonResponse({"data":"All Good Verifier"})
    def post(self, request, format=None):
        # place_id_list = request.POST.getlist('place_id_list')
        place_id_list2 = request.POST.get('place_id_list')
        myDict = request.data
        try:
            place_id_list = myDict['place_id_list']

            place_id = "false_id"
            result_list = dh.get_unique(place_id_list)
            result_error = list()
            result_dict = {
                    "unique_ids": result_list,
                }
            return Response(result_dict,status=status.HTTP_200_OK)
        except CustomError:
            return Response("No results for the place id: "+place_id, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("No results for the place id: "+place_id, status=status.HTTP_400_BAD_REQUEST)

def test_dh(request):
    my_list = dh.create_json_data()
    return JsonResponse({"data":"Tst Dh Good"})

class GetNearbyPlacesLocally(APIView):
    """
    List all countries, or create a new country.
    """
    def get(self, request, format=None):
        # ll = [{"place_id":"EhdQUTM2K0hNLCBOYWlyb2JpLCBLZW55YSImOiQKCg2PPDr_FWtj6RUQChoUChIJp0lN2HIRLxgRTJKXslQCz_c","place_name":"PQ36+HM","category":["street_address"],"address":"PQ36+HM, Nairobi, Kenya","location_coord":"-1.2960625 , 36.7616875","day_hours":"None","phone":"None","website":"None","type_of_data":"scraped","is_test_data":True,"eventId":["FB1010000000000000000000003004"],"error":False}]
        # ll2 = {'html_attributions': [], 'result': {'address_components': [{'long_name': 'Nairobi', 'short_name': 'Nairobi', 'types': ['locality', 'political']}, {'long_name': 'Maziwa', 'short_name': 'Maziwa', 'types': ['sublocality_level_1', 'sublocality', 'political']}, {'long_name': 'Nairobi County', 'short_name': 'Nairobi County', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'Kenya', 'short_name': 'KE', 'types': ['country', 'political']}, {'long_name': '00600', 'short_name': '00600', 'types': ['postal_code']}], 'adr_address': 'kingara Road, <span class="street-address">opp kingara close behind Junction Mall</span>, <span class="postal-code">00600</span>, <span class="locality">Nairobi</span>, <span class="country-name">Kenya</span>', 'business_status': 'OPERATIONAL', 'current_opening_hours': {'open_now': True, 'periods': [{'close': {'date': '2023-04-23', 'day': 0, 'time': '2100'}, 'open': {'date': '2023-04-23', 'day': 0, 'time': '1100'}}, {'close': {'date': '2023-04-24', 'day': 1, 'time': '2100'}, 'open': {'date': '2023-04-24', 'day': 1, 'time': '1100'}}, {'close': {'date': '2023-04-25', 'day': 2, 'time': '2100'}, 'open': {'date': '2023-04-25', 'day': 2, 'time': '1100'}}, {'close': {'date': '2023-04-26', 'day': 3, 'time': '2100'}, 'open': {'date': '2023-04-26', 'day': 3, 'time': '1100'}}, {'close': {'date': '2023-04-27', 'day': 4, 'time': '2100'}, 'open': {'date': '2023-04-27', 'day': 4, 'time': '1100'}}, {'close': {'date': '2023-04-21', 'day': 5, 'time': '2100'}, 'open': {'date': '2023-04-21', 'day': 5, 'time': '1100'}}, {'close': {'date': '2023-04-22', 'day': 6, 'time': '2100'}, 'open': {'date': '2023-04-22', 'day': 6, 'time': '1100'}}], 'weekday_text': ['Monday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Tuesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Wednesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Thursday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Friday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Saturday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Sunday: 11:00\u202fAM\u2009–\u20099:00\u202fPM']}, 'delivery': True, 'dine_in': True, 'formatted_address': 'kingara Road, opp kingara close behind Junction Mall, Nairobi, Kenya', 'formatted_phone_number': '0742 894700', 'geometry': {'location': {'lat': -1.2960063, 'lng': 36.7616708}, 'viewport': {'northeast': {'lat': -1.294604919708498, 'lng': 36.7631173802915}, 'southwest': {'lat': -1.297302880291502, 'lng': 36.76041941970851}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png', 'icon_background_color': '#FF9E67', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet', 'international_phone_number': '+254 742 894700', 'name': 'Whitefield Restaurant', 'opening_hours': {'open_now': True, 'periods': [{'close': {'day': 0, 'time': '2100'}, 'open': {'day': 0, 'time': '1100'}}, {'close': {'day': 1, 'time': '2100'}, 'open': {'day': 1, 'time': '1100'}}, {'close': {'day': 2, 'time': '2100'}, 'open': {'day': 2, 'time': '1100'}}, {'close': {'day': 3, 'time': '2100'}, 'open': {'day': 3, 'time': '1100'}}, {'close': {'day': 4, 'time': '2100'}, 'open': {'day': 4, 'time': '1100'}}, {'close': {'day': 5, 'time': '2100'}, 'open': {'day': 5, 'time': '1100'}}, {'close': {'day': 6, 'time': '2100'}, 'open': {'day': 6, 'time': '1100'}}], 'weekday_text': ['Monday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Tuesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Wednesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Thursday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Friday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Saturday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Sunday: 11:00\u202fAM\u2009–\u20099:00\u202fPM']}, 'photos': [{'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jkATuC0T8GjDwd36b2qFmdvX05LoynTd7UYt21ecQeWWbhro-dFZ1X5fmPWgnYx3St6-5ceQoznAl9kiFDzRBivsyP_rNHc0jA9vHJ0SZ2wwzamP4FcP2Pu_36nSZObngCkWOcLN3UeLo5meFYAGLaWsxhhiJjlX2QcM64ZL9CP1_bP', 'width': 960}, {'height': 2448, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jnZFX2-uMZTgVBBo52uE6iWjdNFAemLYStnV1LOKq5vrrkdfvLF8UR0VPrYgo9ZzNFPkZusndaGms8EGKdgWpU02jL59Hr-HZy0tgpD13AV1ikVuKAWuxury0aLX5H845y_JoKhcbRhknrAT1tKEpUvnqth6heS34IZvjxEf3YDiXUB', 'width': 3264}, {'height': 4032, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/117873843766263809334">Evans Sigei</a>'], 'photo_reference': 'AUjq9jmoR1PWZKV0rA8iYwS2LqOJJRtntAmFwurFxPNWpm8hQft8wZnDk_RcC-RwLdDv7AxsLTeLrFUNB554gZ2sR1xKR1DJ7DzbjNyGF-aOQh43DMSKMqeCOA4k9Ql99LCTTFzU-fnf6wyCAKq0g1i5QxFgNNBrZGMbIbFFt96A4WGQBO1J', 'width': 3024}, {'height': 1650, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jmJff323BYeFMIzMLzJmxYwD-2g0EDLrOpGks_FbmyrcYfqnstiZ5U5TUNDGNuC0hN0qN0lw8qjnTZCcPmfJvJH5Rw6AnSuVcWACS45D3o9SVDEFFMg1tfSF1uudbSLT54w63lh0QXj4SqOtYxISaUusPahxCXSHqxa-v8-yhVo_t6B', 'width': 1275}, {'height': 3264, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/117685926906985511601">Mahim Hegde</a>'], 'photo_reference': 'AUjq9jnWZfCKYMFcUXoOBWghItru6bc8lwZF7QSaAECOUu-JJ684azbtplyQcjnLdsr_ZA6ocM-G-JaXsjMVKPjen_KKAWKCj2-OfYIRc_rlm0o4sEePGf2NDpwitGMxnQ8itKHweK3L4CeiJx-Mn71j1gbGiVnXPpRHiYfk_4UQYPwJ9o3i', 'width': 2448}, {'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jngXTtuMCD-Pt2OmZcwEKS40hC5rpC9fKJxnx0-ZVLv4RWNt38JRWcaz6xGPXBUKf9sdhH51EhciXmYfM2hWvgi3qNAJvQ6LALvAuP6y3bChqLSefLhlAwQuq395cuhTCoviwWZAjFCO6lsKjDo0mekdGlc4TpxXx2nJUytXq3d1IgS', 'width': 960}, {'height': 1280, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jlNsDNyP6iGDW5G0IEJRTUasz4LkHXbw6YEIly95wgh6fzUSYaAKTL2csQ8n3toTuhUQIsVy6ekD2ZjUXQIk4FHLLkjI_-mIsQWQWmefjh867qtQprVjyC7Cn38OMdbiHq0M1GlEbZNmACByoLF_cr3jgOMZ0bbqSq8P3ySlE15A9J5', 'width': 1280}, {'height': 1280, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jkPG8gKWMtee3Ct8KGUDlber9BW4PqCySq8LhSOYJmAYltKg4hnV-n0UejRM91RHEiW1CCDph049QiJ_wNNowXEX0Ozj0nMjyu0PhF6o01k52bO8BvoViUlSdfOUCom_ZGTw48oMKMvkrCPSGzQuJadfA-DOWbPuiubtO6ur9t-XeYG', 'width': 1280}, {'height': 500, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jn9GgvLFriqvar95wBBO9C44wSkVPpD7BMd6ArKwebr9Lyjq-93XbVEPvkP-pWWnYBfJ6XkLiM21a_W7mNqzv_JlzGnGCUs-YFJ4ugFzmUVWupb-aSM8EdntR7RjNg_hKyGOeXqu_HUOBdTCT7aVgawoy4P9H_i7UN_lps_fmqAJ8ub', 'width': 500}, {'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jlkN2f5c9x01-8wd6hVFQZRITX0Rar1RgnKeViKewap2DNzMoY_5QFqchKpWyqyJrSNd7X2elYUGhA-G-qNoH3cCrNDeexeHV3lMragck_96Kfj4crDmjVqDQNvl-jaE79PhkzmESSV6iOySH8s9lgIyr8o-T27LlqL5z0taUxPvbRq', 'width': 960}], 'place_id': 'ChIJj3S0t1IbLxgRYgL-7uH0NIo', 'plus_code': {'compound_code': 'PQ36+HM Nairobi, Kenya', 'global_code': '6GCRPQ36+HM'}, 'price_level': 2, 'rating': 4.3, 'reference': 'ChIJj3S0t1IbLxgRYgL-7uH0NIo', 'reservable': True, 'reviews': [{'author_name': 'David Kanagaretnam', 'author_url': 'https://www.google.com/maps/contrib/109567623568041706461/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5R7RaF1ueYKm_U0ye8jTBBG7K5T3fjTBWQ1MO4BiQ=s128-c0x00000000-cc-rp-mo-ba5', 'rating': 5, 'relative_time_description': 'a year ago', 'text': 'This is a great restaurant for Indian foods mainly however, you will get Kenyan and others too. A calm place to dine with your family and its has a big parking space.  Staff are welcoming and serving the food fast. The place is clean. Prices for food is affordable.', 'time': 1649416437, 'translated': False}, {'author_name': 'Julliet Esta', 'author_url': 'https://www.google.com/maps/contrib/109510066687005858247/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5TQOlQJn_hcLNSJJbB7omg4O-RCyfpbt-4t3unXQls=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 5, 'relative_time_description': '11 months ago', 'text': "We received a warm welcome, service was fast, the food was great and the portions are definitely enough. I would recommend this restaurant for Indian, Chinese and African cuisine, there's a large parking area, kids play area and also a kids menu. The food was also affordable", 'time': 1651396718, 'translated': False}, {'author_name': 'Aoko Gathoni', 'author_url': 'https://www.google.com/maps/contrib/110036374557197962895/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5RHO3ZIMXY_WihCLk7C2xcQcTKdoc5-QhSNkoWh=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 4, 'relative_time_description': '4 months ago', 'text': "When I arrived, the place looked like it wasn't open. But upon asking someone there, he said it was open.\nI ordered for the half koroga chicken with Naan, and to drink, I had tea masala. I liked that their portions were good size.\nI would definitely go back there.", 'time': 1670771464, 'translated': False}, {'author_name': 'Duncanah Gwat', 'author_url': 'https://www.google.com/maps/contrib/116990714119709426524/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5QXiXwls4KibppDfJxM5IHebKyTFfNr5J2j_LoEmw=s128-c0x00000000-cc-rp-mo-ba2', 'rating': 5, 'relative_time_description': '2 months ago',
        # 'text': 'Beutiful place to be, went for a late lunch, nicely ushered in, the waiter was very polite, super helpful. The serve was quick too. The meal was tasty as well', 'time': 1675536564, 'translated': False}, {'author_name': 'B -', 'author_url': 'https://www.google.com/maps/contrib/111323236689199522335/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5Rp3yfS6xwFBSbA9ZvQjd0F50zh5RkWTANNhk44IeI=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 1, 'relative_time_description': '2 weeks ago', 'text': 'Lovely place. Quiet and clean. Polite and friendly staff and they make really good Indian food. The parking is a bit cramped but overall a good intimate experience. The prices are also very agreeable.\n\nI went back recently and standards have plummeted. Its now a really horrible, depressing restaurant that has no identity. It wants to be an Indian restaurant but cant, also Chinese but not happening. Poor service and food that was definitely not fresh.', 'time': 1680543330, 'translated': False}], 'serves_beer': True, 'serves_brunch': True, 'serves_dinner': True, 'serves_lunch': True, 'serves_vegetarian_food': True, 'serves_wine': True, 'takeout': True, 'types': ['restaurant', 'food', 'point_of_interest', 'establishment'], 'url': 'https://maps.google.com/?cid=9958853927237452386', 'user_ratings_total': 171, 'utc_offset': 180, 'vicinity': 'kingara Road, opp kingara close behind Junction Mall, Nairobi', 'website': 'https://whitefieldrestaurant.reserveport.com/', 'wheelchair_accessible_entrance': True}, 'status': 'OK'}
        stored_data = dh.fetch_from_json()
        center_latt = -33.8676569
        center_lonn = 151.
        radius1 = 1000
        radius2 = 2000
        center_loc_str = str(center_latt)+ " , "+str(center_lonn)
        print("center_loc str", center_loc_str)
        stored_data_dict = stored_data[0]
        stored_data_df = pd.DataFrame.from_dict(stored_data_dict)
        stored_data_df['location_coord']=stored_data_df['location_coord'].fillna("0 , 0")
        stored_data_df["hav_distances"] = stored_data_df.apply(lambda x: dh.split_string(center_loc_str, x["location_coord"]), axis = 1)
        wanted_locs_df =  stored_data_df.loc[(stored_data_df['hav_distances'] > radius1) & (stored_data_df['hav_distances'] < radius2)]
        print("=============================================================")
        print(wanted_locs_df[['location_coord','hav_distances']])
        return JsonResponse({"data":"All Good Local Nearby Places"})
    def post(self, request, format=None):
        myDict = request.data
        try:
            ##Retrieve values
            radius1 = myDict['radius1']
            radius2 = myDict['radius2']
            center_latt = myDict['center_lat']
            center_lonn= myDict['center_lon']
            ###Get Data concerned
            stored_data = dh.fetch_from_json()
            stored_data_dict = stored_data[0]
            stored_data_df = pd.DataFrame.from_dict(stored_data_dict)
            stored_data_df['location_coord']=stored_data_df['location_coord'].fillna(0)
            stored_data_df["hav_distances"] = stored_data_df.apply(lambda x: dh.split_string(str(center_latt)+ " , "+str(center_lonn), x["location_coord"]), axis = 1)
            result_list = []
            result_error = list()
            result_dict = {
                    "unique_ids": result_list,
                }
            return Response(result_dict,status=status.HTTP_200_OK)
        except CustomError:
            return Response("No results for the place id: "+"place_id", status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("No results for the place id: "+"place_id", status=status.HTTP_400_BAD_REQUEST)
