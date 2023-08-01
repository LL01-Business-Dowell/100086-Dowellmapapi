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
from datetime import datetime
import googlemaps
from decouple import config
api_key = config("API_KEY")
# Create your views here.
import time
# while True:
    # Code executed here
    # dh.create_json_data()
    # now = datetime.now()

    # current_time = now.strftime("%H:%M:%S")
    # print("Current Time Refreshing =", current_time)
    # print("Time now", )
    # time.sleep(300)
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
def retrieve_details(results_1, plc_id, is_test_data, center_loc = ""):
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
    photo_reference ='None'
    rating = 'None'
    distance_from_center = 'None'
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
            # loc_str = str(lat)+ " , "+str(lng)
            # if center_loc != '':
                # distance_from_center = dh.split_string(loc_str, center_loc)
                # distance_from_center = dh.get_distance(loc_str, center_loc)
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
        if 'photos' in results:
            # print(results['place_id'])
            photo_reference = results['photos'][0]['photo_reference']
        if "rating" in results:
            # print(results['place_id'])
            rating = results["rating"]


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
     "photo_reference":photo_reference,
     "rating":rating,
    "type_of_data": "scraped",
    # "distance_from_center":distance_from_center,
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
        return JsonResponse({"status":"Kindly use a POST request instead of GET"})
    def post(self, request):
        place_id = request.data.get('place_id')
        url='https://maps.googleapis.com/maps/api/place/details/json?placeid='+place_id+'&key='+api_key


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
        return JsonResponse({"data":"Kindly use a POST request instead of GET"})
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
            wanted_api_key = myDict['api_key']
            print("wanted_api_key ------>>> ", wanted_api_key)
            type_error_message = "Invalid key."
            res = dh.processApikey(wanted_api_key)
            if res.status_code == 400:
                result = json.loads(res.text)
                type_error_message = type_error_message + " "+result["message"]
                # raise CustomError(type_error_message)
                return Response(type_error_message,status=status.HTTP_400_BAD_REQUEST)
            for plc_id in place_id_list:
                place_id = plc_id

                url='https://maps.googleapis.com/maps/api/place/details/json?placeid='+place_id+'&key='+api_key

                r=requests.get(url)
                results = json.loads(r.text)
                print("raw results a new no stage============")
                print(results)
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
                    total_succ_saved.append(result_list[i]['placeId'])
                else:
                    error_message = "Could not insert for : "+result_list[i]['placeId']
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
        return JsonResponse({"data":"Kindly use a POST request instead of GET"})
    def post(self, request, format=None):
        # place_id_list = request.POST.getlist('place_id_list')
        # place_id_list2 = request.POST.get('place_id_list')
        myDict = request.data
        place_id_list = myDict['place_id_list']
        center_loc = 'None'
        # if "center_loc" in myDict:
            # center_loc = myDict["center_loc"]
        total_succ_queried=list()
        total_failed_queried = list()
        total_succ_saved = list()
        place_id = ''
        result_list = list()
        result_error = list()
        # print("raw POSY============")
        # print(list(request.POST.items()))
        # print("raw rquest============")
        # print(place_id_list)
        # print(type(place_id_list))
        # print("raw rquest2============")
        # print(place_id_list2)
        # print(type(place_id_list2))
        # print("raw simplejspn============")
        # print(myDict)
        # print(type(myDict))



        try:
            wanted_api_key = myDict['api_key']
            print("wanted_api_key ------>>> ", wanted_api_key)
            type_error_message = "Invalid key."
            res = dh.processApikey(wanted_api_key)
            if res.status_code == 400:
                result = json.loads(res.text)
                type_error_message = type_error_message + " "+result["message"]
                # raise CustomError(type_error_message)
                return Response(type_error_message,status=status.HTTP_400_BAD_REQUEST)
            for plc_id in place_id_list:
                place_id = plc_id
                url='https://maps.googleapis.com/maps/api/place/details/json?placeid='+place_id+'&key='+api_key

                r=requests.get(url)
                results = json.loads(r.text)
                # print("raw results new stage 1============")
                # print(results)
                # if center_loc != 'None':
                resp = retrieve_details(results, plc_id, True, center_loc)
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



class SavePlacesDetail(APIView):
    """
    List all countries, or create a new country.
    """
    def get(self, request, format=None):
        # ll = [{"place_id":"EhdQUTM2K0hNLCBOYWlyb2JpLCBLZW55YSImOiQKCg2PPDr_FWtj6RUQChoUChIJp0lN2HIRLxgRTJKXslQCz_c","place_name":"PQ36+HM","category":["street_address"],"address":"PQ36+HM, Nairobi, Kenya","location_coord":"-1.2960625 , 36.7616875","day_hours":"None","phone":"None","website":"None","type_of_data":"scraped","is_test_data":True,"eventId":["FB1010000000000000000000003004"],"error":False}]
        # ll2 = {'html_attributions': [], 'result': {'address_components': [{'long_name': 'Nairobi', 'short_name': 'Nairobi', 'types': ['locality', 'political']}, {'long_name': 'Maziwa', 'short_name': 'Maziwa', 'types': ['sublocality_level_1', 'sublocality', 'political']}, {'long_name': 'Nairobi County', 'short_name': 'Nairobi County', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'Kenya', 'short_name': 'KE', 'types': ['country', 'political']}, {'long_name': '00600', 'short_name': '00600', 'types': ['postal_code']}], 'adr_address': 'kingara Road, <span class="street-address">opp kingara close behind Junction Mall</span>, <span class="postal-code">00600</span>, <span class="locality">Nairobi</span>, <span class="country-name">Kenya</span>', 'business_status': 'OPERATIONAL', 'current_opening_hours': {'open_now': True, 'periods': [{'close': {'date': '2023-04-23', 'day': 0, 'time': '2100'}, 'open': {'date': '2023-04-23', 'day': 0, 'time': '1100'}}, {'close': {'date': '2023-04-24', 'day': 1, 'time': '2100'}, 'open': {'date': '2023-04-24', 'day': 1, 'time': '1100'}}, {'close': {'date': '2023-04-25', 'day': 2, 'time': '2100'}, 'open': {'date': '2023-04-25', 'day': 2, 'time': '1100'}}, {'close': {'date': '2023-04-26', 'day': 3, 'time': '2100'}, 'open': {'date': '2023-04-26', 'day': 3, 'time': '1100'}}, {'close': {'date': '2023-04-27', 'day': 4, 'time': '2100'}, 'open': {'date': '2023-04-27', 'day': 4, 'time': '1100'}}, {'close': {'date': '2023-04-21', 'day': 5, 'time': '2100'}, 'open': {'date': '2023-04-21', 'day': 5, 'time': '1100'}}, {'close': {'date': '2023-04-22', 'day': 6, 'time': '2100'}, 'open': {'date': '2023-04-22', 'day': 6, 'time': '1100'}}], 'weekday_text': ['Monday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Tuesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Wednesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Thursday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Friday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Saturday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Sunday: 11:00\u202fAM\u2009–\u20099:00\u202fPM']}, 'delivery': True, 'dine_in': True, 'formatted_address': 'kingara Road, opp kingara close behind Junction Mall, Nairobi, Kenya', 'formatted_phone_number': '0742 894700', 'geometry': {'location': {'lat': -1.2960063, 'lng': 36.7616708}, 'viewport': {'northeast': {'lat': -1.294604919708498, 'lng': 36.7631173802915}, 'southwest': {'lat': -1.297302880291502, 'lng': 36.76041941970851}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png', 'icon_background_color': '#FF9E67', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet', 'international_phone_number': '+254 742 894700', 'name': 'Whitefield Restaurant', 'opening_hours': {'open_now': True, 'periods': [{'close': {'day': 0, 'time': '2100'}, 'open': {'day': 0, 'time': '1100'}}, {'close': {'day': 1, 'time': '2100'}, 'open': {'day': 1, 'time': '1100'}}, {'close': {'day': 2, 'time': '2100'}, 'open': {'day': 2, 'time': '1100'}}, {'close': {'day': 3, 'time': '2100'}, 'open': {'day': 3, 'time': '1100'}}, {'close': {'day': 4, 'time': '2100'}, 'open': {'day': 4, 'time': '1100'}}, {'close': {'day': 5, 'time': '2100'}, 'open': {'day': 5, 'time': '1100'}}, {'close': {'day': 6, 'time': '2100'}, 'open': {'day': 6, 'time': '1100'}}], 'weekday_text': ['Monday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Tuesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Wednesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Thursday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Friday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Saturday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Sunday: 11:00\u202fAM\u2009–\u20099:00\u202fPM']}, 'photos': [{'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jkATuC0T8GjDwd36b2qFmdvX05LoynTd7UYt21ecQeWWbhro-dFZ1X5fmPWgnYx3St6-5ceQoznAl9kiFDzRBivsyP_rNHc0jA9vHJ0SZ2wwzamP4FcP2Pu_36nSZObngCkWOcLN3UeLo5meFYAGLaWsxhhiJjlX2QcM64ZL9CP1_bP', 'width': 960}, {'height': 2448, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jnZFX2-uMZTgVBBo52uE6iWjdNFAemLYStnV1LOKq5vrrkdfvLF8UR0VPrYgo9ZzNFPkZusndaGms8EGKdgWpU02jL59Hr-HZy0tgpD13AV1ikVuKAWuxury0aLX5H845y_JoKhcbRhknrAT1tKEpUvnqth6heS34IZvjxEf3YDiXUB', 'width': 3264}, {'height': 4032, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/117873843766263809334">Evans Sigei</a>'], 'photo_reference': 'AUjq9jmoR1PWZKV0rA8iYwS2LqOJJRtntAmFwurFxPNWpm8hQft8wZnDk_RcC-RwLdDv7AxsLTeLrFUNB554gZ2sR1xKR1DJ7DzbjNyGF-aOQh43DMSKMqeCOA4k9Ql99LCTTFzU-fnf6wyCAKq0g1i5QxFgNNBrZGMbIbFFt96A4WGQBO1J', 'width': 3024}, {'height': 1650, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jmJff323BYeFMIzMLzJmxYwD-2g0EDLrOpGks_FbmyrcYfqnstiZ5U5TUNDGNuC0hN0qN0lw8qjnTZCcPmfJvJH5Rw6AnSuVcWACS45D3o9SVDEFFMg1tfSF1uudbSLT54w63lh0QXj4SqOtYxISaUusPahxCXSHqxa-v8-yhVo_t6B', 'width': 1275}, {'height': 3264, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/117685926906985511601">Mahim Hegde</a>'], 'photo_reference': 'AUjq9jnWZfCKYMFcUXoOBWghItru6bc8lwZF7QSaAECOUu-JJ684azbtplyQcjnLdsr_ZA6ocM-G-JaXsjMVKPjen_KKAWKCj2-OfYIRc_rlm0o4sEePGf2NDpwitGMxnQ8itKHweK3L4CeiJx-Mn71j1gbGiVnXPpRHiYfk_4UQYPwJ9o3i', 'width': 2448}, {'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jngXTtuMCD-Pt2OmZcwEKS40hC5rpC9fKJxnx0-ZVLv4RWNt38JRWcaz6xGPXBUKf9sdhH51EhciXmYfM2hWvgi3qNAJvQ6LALvAuP6y3bChqLSefLhlAwQuq395cuhTCoviwWZAjFCO6lsKjDo0mekdGlc4TpxXx2nJUytXq3d1IgS', 'width': 960}, {'height': 1280, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jlNsDNyP6iGDW5G0IEJRTUasz4LkHXbw6YEIly95wgh6fzUSYaAKTL2csQ8n3toTuhUQIsVy6ekD2ZjUXQIk4FHLLkjI_-mIsQWQWmefjh867qtQprVjyC7Cn38OMdbiHq0M1GlEbZNmACByoLF_cr3jgOMZ0bbqSq8P3ySlE15A9J5', 'width': 1280}, {'height': 1280, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jkPG8gKWMtee3Ct8KGUDlber9BW4PqCySq8LhSOYJmAYltKg4hnV-n0UejRM91RHEiW1CCDph049QiJ_wNNowXEX0Ozj0nMjyu0PhF6o01k52bO8BvoViUlSdfOUCom_ZGTw48oMKMvkrCPSGzQuJadfA-DOWbPuiubtO6ur9t-XeYG', 'width': 1280}, {'height': 500, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jn9GgvLFriqvar95wBBO9C44wSkVPpD7BMd6ArKwebr9Lyjq-93XbVEPvkP-pWWnYBfJ6XkLiM21a_W7mNqzv_JlzGnGCUs-YFJ4ugFzmUVWupb-aSM8EdntR7RjNg_hKyGOeXqu_HUOBdTCT7aVgawoy4P9H_i7UN_lps_fmqAJ8ub', 'width': 500}, {'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jlkN2f5c9x01-8wd6hVFQZRITX0Rar1RgnKeViKewap2DNzMoY_5QFqchKpWyqyJrSNd7X2elYUGhA-G-qNoH3cCrNDeexeHV3lMragck_96Kfj4crDmjVqDQNvl-jaE79PhkzmESSV6iOySH8s9lgIyr8o-T27LlqL5z0taUxPvbRq', 'width': 960}], 'place_id': 'ChIJj3S0t1IbLxgRYgL-7uH0NIo', 'plus_code': {'compound_code': 'PQ36+HM Nairobi, Kenya', 'global_code': '6GCRPQ36+HM'}, 'price_level': 2, 'rating': 4.3, 'reference': 'ChIJj3S0t1IbLxgRYgL-7uH0NIo', 'reservable': True, 'reviews': [{'author_name': 'David Kanagaretnam', 'author_url': 'https://www.google.com/maps/contrib/109567623568041706461/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5R7RaF1ueYKm_U0ye8jTBBG7K5T3fjTBWQ1MO4BiQ=s128-c0x00000000-cc-rp-mo-ba5', 'rating': 5, 'relative_time_description': 'a year ago', 'text': 'This is a great restaurant for Indian foods mainly however, you will get Kenyan and others too. A calm place to dine with your family and its has a big parking space.  Staff are welcoming and serving the food fast. The place is clean. Prices for food is affordable.', 'time': 1649416437, 'translated': False}, {'author_name': 'Julliet Esta', 'author_url': 'https://www.google.com/maps/contrib/109510066687005858247/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5TQOlQJn_hcLNSJJbB7omg4O-RCyfpbt-4t3unXQls=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 5, 'relative_time_description': '11 months ago', 'text': "We received a warm welcome, service was fast, the food was great and the portions are definitely enough. I would recommend this restaurant for Indian, Chinese and African cuisine, there's a large parking area, kids play area and also a kids menu. The food was also affordable", 'time': 1651396718, 'translated': False}, {'author_name': 'Aoko Gathoni', 'author_url': 'https://www.google.com/maps/contrib/110036374557197962895/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5RHO3ZIMXY_WihCLk7C2xcQcTKdoc5-QhSNkoWh=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 4, 'relative_time_description': '4 months ago', 'text': "When I arrived, the place looked like it wasn't open. But upon asking someone there, he said it was open.\nI ordered for the half koroga chicken with Naan, and to drink, I had tea masala. I liked that their portions were good size.\nI would definitely go back there.", 'time': 1670771464, 'translated': False}, {'author_name': 'Duncanah Gwat', 'author_url': 'https://www.google.com/maps/contrib/116990714119709426524/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5QXiXwls4KibppDfJxM5IHebKyTFfNr5J2j_LoEmw=s128-c0x00000000-cc-rp-mo-ba2', 'rating': 5, 'relative_time_description': '2 months ago',
        # 'text': 'Beutiful place to be, went for a late lunch, nicely ushered in, the waiter was very polite, super helpful. The serve was quick too. The meal was tasty as well', 'time': 1675536564, 'translated': False}, {'author_name': 'B -', 'author_url': 'https://www.google.com/maps/contrib/111323236689199522335/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5Rp3yfS6xwFBSbA9ZvQjd0F50zh5RkWTANNhk44IeI=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 1, 'relative_time_description': '2 weeks ago', 'text': 'Lovely place. Quiet and clean. Polite and friendly staff and they make really good Indian food. The parking is a bit cramped but overall a good intimate experience. The prices are also very agreeable.\n\nI went back recently and standards have plummeted. Its now a really horrible, depressing restaurant that has no identity. It wants to be an Indian restaurant but cant, also Chinese but not happening. Poor service and food that was definitely not fresh.', 'time': 1680543330, 'translated': False}], 'serves_beer': True, 'serves_brunch': True, 'serves_dinner': True, 'serves_lunch': True, 'serves_vegetarian_food': True, 'serves_wine': True, 'takeout': True, 'types': ['restaurant', 'food', 'point_of_interest', 'establishment'], 'url': 'https://maps.google.com/?cid=9958853927237452386', 'user_ratings_total': 171, 'utc_offset': 180, 'vicinity': 'kingara Road, opp kingara close behind Junction Mall, Nairobi', 'website': 'https://whitefieldrestaurant.reserveport.com/', 'wheelchair_accessible_entrance': True}, 'status': 'OK'}
        return JsonResponse({"data":"Kindly use a POST request instead of GET"})
    def post(self, request, format=None):
        # place_id_list = request.POST.getlist('place_id_list')
        # result_dict = request.POST.get('result_dict')
        myDict = request.data
        result_dict = myDict['result_dict']
        wanted_api_key = myDict['api_key']
        print("wanted_api_key ------>>> ", wanted_api_key)
        type_error_message = "Invalid key."
        res = dh.processApikey(wanted_api_key)
        if res.status_code == 400:
            result = json.loads(res.text)
            type_error_message = type_error_message + " "+result["message"]
            # raise CustomError(type_error_message)
            return Response(type_error_message,status=status.HTTP_400_BAD_REQUEST)
        else:
            type_error_message = "Invalid payload "
        total_succ_queried=list()
        total_failed_queried = list()
        total_succ_saved = list()
        place_id = ''
        result_list = result_dict['succesful_results']
        result_error = list()
        # print("raw POSY============")
        # print(list(request.POST.items()))
        # print(myDict)
        # print(type(myDict))



        try:
            print("FIrst return succesfully")
            success_mess = "Sent Succesfully"
            return Response(success_mess,status=status.HTTP_200_OK)
        except CustomError:
            return Response(type_error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response(type_error_message, status=status.HTTP_400_BAD_REQUEST)
        finally:
            print("In the finally")
            try:
                success_mess = "Saved Succesfully"
                wanted_api_key = myDict['api_key']
                print("wanted_api_key ------>>> ", wanted_api_key)
                type_error_message = "Invalid key."
                res = dh.processApikey(wanted_api_key)
                if res.status_code == 400:
                    result = json.loads(res.text)
                    type_error_message = type_error_message + " "+result["message"]
                    raise CustomError(type_error_message)
                else:
                    type_error_message = "Invalid payload "
                for i in range(len(result_list)):
                    re = dh.insert_data(result_list[i])
                    temp_plc_id = ""
                    if 'placeId' in result_list[i]:
                        temp_plc_id = result_list[i]['placeId']
                    if 'place_id' in result_list[i]:
                        temp_plc_id = result_list[i]['place_id']
                    if re["isSuccess"]:
                        print("ReqData intserted:  --> insert Id: "+str(re["inserted_id"]))
                        print("Reseult slist", result_list)


                        total_succ_saved.append(temp_plc_id)
                    else:
                        error_message = "Could not insert for : "+temp_plc_id
                        +". Error from server : "+str(re['error'])+"Successful inserted : "
                        +preparing_list_for_error_message(total_succ_saved)+"Succesful queried :"
                        +preparing_list_for_error_message(total_succ_queried)+"Unsucceful queried are : "+preparing_list_for_error_message(total_failed_queried)
                    # error_message = "Could not insert for : "+place_id_list[0]+". Error from server : "+str(True)+"Successful inserted : "+preparing_list_for_error_message(total_succ_saved)+"Succesful queried : "+preparing_list_for_error_message(total_succ_queried)+"Unsuccefull queried : "+preparing_list_for_error_message(total_failed_queried)
                        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
                return Response(success_mess,status=status.HTTP_200_OK)
            except CustomError:
                return Response(type_error_message, status=status.HTTP_400_BAD_REQUEST)
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
        try:
            # data = dh.get_unique_from_mongo("s")
            # res = dh.processApikey("3f")
            # print("res.code ====== ",res.status_code)
            # print("res.text ====== ",res.text)
            return JsonResponse({"info":"Kindly use a POST request instead of GET", "res":res})
        # except Exception as ex:
        #     print("Handle erroes++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        #     template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        #     message = template.format(type(ex).__name__, ex.args)
        #     print (message)
        except CustomError:
            return Response("No results for the place id: ", status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("No results for the place id: ", status=status.HTTP_400_BAD_REQUEST)
        # finally:

        #     print("Another line finally run --------------------------------------->>>>>>>>>>>")

    def post(self, request, format=None):
        # place_id_list = request.POST.getlist('place_id_list')
        # place_id_list2 = request.POST.get('place_id_list')
        myDict = request.data

        try:
            wanted_api_key = myDict['api_key']
            print("wanted_api_key ------>>> ", wanted_api_key)
            type_error_message = "Invalid key."
            res = dh.processApikey(wanted_api_key)
            if res.status_code == 400:
                result = json.loads(res.text)
                type_error_message = type_error_message + " "+result["message"]
                raise CustomError(type_error_message)
            else:
                type_error_message = "Invalid payload "
            place_id_list = myDict['place_id_list']

            place_id = "false_id"
            result_list = dh.get_unique_from_mongo(place_id_list)
            result_error = list()
            result_dict = {
                    "unique_ids": result_list,
                }
            print("unique_ids",result_dict)
            return Response(result_dict,status=status.HTTP_200_OK)
        except CustomError:
            return Response(type_error_message, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("No results for the place id: "+place_id, status=status.HTTP_400_BAD_REQUEST)

def refresh_json_dh(request):
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
        return JsonResponse({"info":"Kindly use a POST request instead of GET"})
    def post(self, request, format=None):
        myDict = request.data
        try:
            ##Retrieve values
            wanted_api_key = myDict['api_key']
            print("wanted_api_key ------>>> ", wanted_api_key)
            type_error_message = "Invalid key."

            res = dh.processApikey(wanted_api_key)
            if res.status_code == 400:
                result = json.loads(res.text)
                type_error_message = type_error_message + " "+result["message"]
                # raise CustomError(type_error_message)
                return Response(type_error_message,status=status.HTTP_400_BAD_REQUEST)
            type_error_message = "Kindly check if the parameter"
            radius1 = myDict['radius1']
            radius2 = myDict['radius2']
            center_latt = myDict['center_lat']
            center_lonn= myDict['center_lon']
            search_string = myDict['query_string']
            data_type = myDict['data_type']
            type_error_message = "Wrong parameter type for radius1 should be of a float/int type."
            radius1 = float(radius1)
            type_error_message = "Wrong parameter type for radius2 should be of a float/int type."
            radius2 = float(radius2)
            type_error_message = "Wrong parameter type for center_latt should be of a float type."
            center_latt = float(center_latt)
            type_error_message = "Wrong parameter type for center_lonn should be of a float type."
            center_lonn = float(center_lonn)
            type_error_message = "Wrong parameter type for search_string should be of a string type."
            if  not isinstance(search_string, str):
                raise ValueError(type_error_message)
            # search_string = str(search_string)
            type_error_message = "Wrong parameter type for data_type should be of a string type and should be equal to 'registered'/'scraped'/'all'."
            if  not isinstance(data_type, str):
                raise ValueError(type_error_message)
            if data_type != "registered"  and data_type != "scraped" and data_type != "all":
                raise ValueError(type_error_message)
            center_loc_str = str(center_latt)+ " , "+str(center_lonn)
            ###Get Data concerned
            # stored_data = dh.fetch_from_json()
            stored_data = dh.fetch_from_mongo()
            stored_data_dict = stored_data[0]
            # stored_data_df = pd.DataFrame.from_dict(stored_data_dict, index=[0])
            stored_data_df = pd.DataFrame(stored_data)
            stored_data_df['location_coord']=stored_data_df['location_coord'].fillna("0 , 0")
            stored_data_df["hav_distances"] = stored_data_df.apply(lambda x: dh.split_string(center_loc_str, x["location_coord"]), axis = 1)
            wanted_locs_df =  stored_data_df.loc[(stored_data_df['hav_distances'] >= radius1) & (stored_data_df['hav_distances'] <= radius2)]
            if len(wanted_locs_df):
                wanted_locs_df['category'].fillna("None", inplace=True)
                print("wanted_locs_df lenfght = ", len(wanted_locs_df))
                print("wanted_locs_df  = ", wanted_locs_df[['category']])
                wanted_locs_df = wanted_locs_df[wanted_locs_df['category'].apply(lambda x: search_string in x)]
                if len(wanted_locs_df):
                    wanted_locs_df =  wanted_locs_df.loc[wanted_locs_df['type_of_data'] == data_type]
                    if len(wanted_locs_df):
                        print("============================POST=================================")
                    # print(wanted_locs_df[['location_coord','hav_distances', 'category', 'placeId']])
                        print("=============================Inteded to be sean================================")
                        wanted_locs_df['place_id'].fillna("None", inplace=True)
                        wanted_locs_df['placeId'].fillna("None", inplace=True)
                        wanted_locs_df['category'].fillna("None", inplace=True)
                        print(wanted_locs_df[['category']].head())
                        print("============================end of scenrary=================================")
                        wanted_dict = wanted_locs_df[['location_coord','hav_distances', 'category', 'placeId','place_id', 'place_name']].to_dict('records')
                        print("type_wanted_dict[0]['place_name]",type(wanted_dict[0]['place_name']))
                        print("type_wanted_dict[0]['location_coord]",type(wanted_dict[0]['location_coord']))
                        wanted_list = list()
                        place_name_list = list()
                        loc_list = list()
                        for i in wanted_dict:
                            if i['place_name'] not in place_name_list or i['location_coord'] not in loc_list:
                                place_name_list.append(i['place_name'] )
                                loc_list.append(i['location_coord'] )
                                wanted_list.append(i)

                # new_wanted_dict = [dict(t) for t in {tuple(d.items()) for d in wanted_dict}]
        # using two maps()
            # list(map(lambda t: dict(t), set(list(map(lambda d: tuple(d.items()), l)))))
                        print("wanted locs columns",wanted_locs_df.columns)
                # wanted_dict = wanted_locs_df[['location_coord','hav_distances', 'category', 'placeId']].to_dict('records')
                        result_dict = {
                        "data":wanted_list
                        }
                        return Response(result_dict,status=status.HTTP_200_OK)
                    else:
                        result_dict = {
                        "message": "Currently, there are no stored locations for the center and distance range in the payload you sent.",
                        "data": []
                        }
                        return Response(result_dict,status=status.HTTP_200_OK)

                else:
                    result_dict = {
                        "message": "Currently, there are no stored locations for the center and distance range in the payload you sent.",
                        "data": []
                        }
                    return Response(result_dict,status=status.HTTP_200_OK)
            else:
                result_dict = {
                        "data": []
                        }
                return Response(result_dict,status=status.HTTP_200_OK)
        except ValueError:
            return Response(type_error_message, status=status.HTTP_400_BAD_REQUEST)
        except CustomError:
            return Response("Kindly check your query inputs", status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly check your query inputs", status=status.HTTP_400_BAD_REQUEST)
class GetNearbyPlacesLocallyV2(APIView):
    def get(self, request, format=None):
        return JsonResponse({"info":"Kindly use a POST request instead of GET Version 2"})
    def post(self, request, format=None):

        gmaps = googlemaps.Client(key=api_key)
        myDict = request.data
        try:
            ##Retrieve values
            type_error_message = "Kindly check if the parameter"
            radius1 = myDict['radius1']
            radius2 = myDict['radius2']

            center_latt = myDict['center_lat']
            center_lonn= myDict['center_lon']
            search_string = myDict['query_string']
            limit = myDict['limit']
            wanted_api_key = myDict['api_key']
            print("wanted_api_key ------>>> ", wanted_api_key)
            type_error_message = "Invalid key."
            res = dh.processApikey(wanted_api_key)
            if res.status_code == 400:
                raise ValueError(type_error_message)

            type_error_message = "Wrong parameter type for radius1 should be of a float/int type."
            radius1 = float(radius1)
            type_error_message = "Wrong parameter type for radius2 should be of a float/int type."
            radius2 = float(radius2)
            if radius2 <= 0:
                payload_2 = {
                "place_id_list":[]
            }
                return Response(payload_2,status=status.HTTP_200_OK)
            type_error_message = "Wrong parameter type for center_latt should be of a float type."
            center_latt = float(center_latt)
            type_error_message = "Wrong parameter type for center_lonn should be of a float type."
            center_lonn = float(center_lonn)
            type_error_message = "Wrong parameter type for search_string should be of a string type."
            if  not isinstance(search_string, str):
                raise ValueError(type_error_message)
            # search_string = str(search_string)
            type_error_message = "Wrong parameter type for data_type should be of a int type and should be equal to '20'/'40'/'60'."
            limit = int(limit)
            if limit != 20  and limit != 40 and limit != 60:
                raise ValueError(type_error_message)
            center_loc_str = str(center_latt)+ " , "+str(center_lonn)
                # wanted_dict = wanted_locs_df[['location_coord','hav_distances', 'category', 'placeId']].to_dict('records')
            check = True
            t = 0
            page_tok = 0
            wanted_list = []
            place_id_list =[]
            count_res = limit

            while check:
                t = t+1
                print("t == ", t)
                params = {
        'query': [ search_string ],
        'location': (center_latt,center_lonn),
        'radius': radius2
    }
                if t >1:
                    params['page_token'] = page_tok
                print("page_tok = ",page_tok)
                time.sleep(2)
                r_json =gmaps.places(**params)
                count_res -= 20
                wanted_list.extend(r_json['results'])


                if count_res == 0:
                    check = False
                else:
                    if 'next_page_token' in r_json:
                        page_tok =r_json['next_page_token']
                    else:
                        check = False

            print("laenghth og wanted list post", len(wanted_list))
            for i in wanted_list:
                place_id_list.append(i['place_id'])
            print("laenghth og place_id_list post", len(place_id_list))
            print("place_id_list post", place_id_list)
            payload_2 = {
                "place_id_list":place_id_list,
                "center_loc":center_loc_str
            }
            # res = requests.post('https://100086.pythonanywhere.com/accounts/get-details-list-stage1/',json=payload_2)
            print("-------------------------------------------------------------------------------")
            # print(res.text)
            # print(type(res.text))
            # print(json.loads(res.text))
            # result = json.loads(res.text)
            # print(type(result))

            return Response(payload_2,status=status.HTTP_200_OK)
        except ValueError:
            return Response(type_error_message, status=status.HTTP_400_BAD_REQUEST)
        except CustomError:
            return Response("Kindly check your query inputs", status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response("Kindly check your query inputs", status=status.HTTP_400_BAD_REQUEST)


def show_mongo_data(request):
    needed_m_data = dh.fetch_from_mongo()
    return JsonResponse({"data":needed_m_data})
def show_json_data(request):
    needed_m_data = dh.fetch_from_registered_json()
    return JsonResponse({"data":needed_m_data})
class TestLocalDistance(APIView):
    """
    List all countries, or create a new country.
    """
    def get(self, request, format=None):
        # ll = [{"place_id":"EhdQUTM2K0hNLCBOYWlyb2JpLCBLZW55YSImOiQKCg2PPDr_FWtj6RUQChoUChIJp0lN2HIRLxgRTJKXslQCz_c","place_name":"PQ36+HM","category":["street_address"],"address":"PQ36+HM, Nairobi, Kenya","location_coord":"-1.2960625 , 36.7616875","day_hours":"None","phone":"None","website":"None","type_of_data":"scraped","is_test_data":True,"eventId":["FB1010000000000000000000003004"],"error":False}]
        # ll2 = {'html_attributions': [], 'result': {'address_components': [{'long_name': 'Nairobi', 'short_name': 'Nairobi', 'types': ['locality', 'political']}, {'long_name': 'Maziwa', 'short_name': 'Maziwa', 'types': ['sublocality_level_1', 'sublocality', 'political']}, {'long_name': 'Nairobi County', 'short_name': 'Nairobi County', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'Kenya', 'short_name': 'KE', 'types': ['country', 'political']}, {'long_name': '00600', 'short_name': '00600', 'types': ['postal_code']}], 'adr_address': 'kingara Road, <span class="street-address">opp kingara close behind Junction Mall</span>, <span class="postal-code">00600</span>, <span class="locality">Nairobi</span>, <span class="country-name">Kenya</span>', 'business_status': 'OPERATIONAL', 'current_opening_hours': {'open_now': True, 'periods': [{'close': {'date': '2023-04-23', 'day': 0, 'time': '2100'}, 'open': {'date': '2023-04-23', 'day': 0, 'time': '1100'}}, {'close': {'date': '2023-04-24', 'day': 1, 'time': '2100'}, 'open': {'date': '2023-04-24', 'day': 1, 'time': '1100'}}, {'close': {'date': '2023-04-25', 'day': 2, 'time': '2100'}, 'open': {'date': '2023-04-25', 'day': 2, 'time': '1100'}}, {'close': {'date': '2023-04-26', 'day': 3, 'time': '2100'}, 'open': {'date': '2023-04-26', 'day': 3, 'time': '1100'}}, {'close': {'date': '2023-04-27', 'day': 4, 'time': '2100'}, 'open': {'date': '2023-04-27', 'day': 4, 'time': '1100'}}, {'close': {'date': '2023-04-21', 'day': 5, 'time': '2100'}, 'open': {'date': '2023-04-21', 'day': 5, 'time': '1100'}}, {'close': {'date': '2023-04-22', 'day': 6, 'time': '2100'}, 'open': {'date': '2023-04-22', 'day': 6, 'time': '1100'}}], 'weekday_text': ['Monday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Tuesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Wednesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Thursday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Friday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Saturday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Sunday: 11:00\u202fAM\u2009–\u20099:00\u202fPM']}, 'delivery': True, 'dine_in': True, 'formatted_address': 'kingara Road, opp kingara close behind Junction Mall, Nairobi, Kenya', 'formatted_phone_number': '0742 894700', 'geometry': {'location': {'lat': -1.2960063, 'lng': 36.7616708}, 'viewport': {'northeast': {'lat': -1.294604919708498, 'lng': 36.7631173802915}, 'southwest': {'lat': -1.297302880291502, 'lng': 36.76041941970851}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png', 'icon_background_color': '#FF9E67', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet', 'international_phone_number': '+254 742 894700', 'name': 'Whitefield Restaurant', 'opening_hours': {'open_now': True, 'periods': [{'close': {'day': 0, 'time': '2100'}, 'open': {'day': 0, 'time': '1100'}}, {'close': {'day': 1, 'time': '2100'}, 'open': {'day': 1, 'time': '1100'}}, {'close': {'day': 2, 'time': '2100'}, 'open': {'day': 2, 'time': '1100'}}, {'close': {'day': 3, 'time': '2100'}, 'open': {'day': 3, 'time': '1100'}}, {'close': {'day': 4, 'time': '2100'}, 'open': {'day': 4, 'time': '1100'}}, {'close': {'day': 5, 'time': '2100'}, 'open': {'day': 5, 'time': '1100'}}, {'close': {'day': 6, 'time': '2100'}, 'open': {'day': 6, 'time': '1100'}}], 'weekday_text': ['Monday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Tuesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Wednesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Thursday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Friday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Saturday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Sunday: 11:00\u202fAM\u2009–\u20099:00\u202fPM']}, 'photos': [{'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jkATuC0T8GjDwd36b2qFmdvX05LoynTd7UYt21ecQeWWbhro-dFZ1X5fmPWgnYx3St6-5ceQoznAl9kiFDzRBivsyP_rNHc0jA9vHJ0SZ2wwzamP4FcP2Pu_36nSZObngCkWOcLN3UeLo5meFYAGLaWsxhhiJjlX2QcM64ZL9CP1_bP', 'width': 960}, {'height': 2448, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jnZFX2-uMZTgVBBo52uE6iWjdNFAemLYStnV1LOKq5vrrkdfvLF8UR0VPrYgo9ZzNFPkZusndaGms8EGKdgWpU02jL59Hr-HZy0tgpD13AV1ikVuKAWuxury0aLX5H845y_JoKhcbRhknrAT1tKEpUvnqth6heS34IZvjxEf3YDiXUB', 'width': 3264}, {'height': 4032, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/117873843766263809334">Evans Sigei</a>'], 'photo_reference': 'AUjq9jmoR1PWZKV0rA8iYwS2LqOJJRtntAmFwurFxPNWpm8hQft8wZnDk_RcC-RwLdDv7AxsLTeLrFUNB554gZ2sR1xKR1DJ7DzbjNyGF-aOQh43DMSKMqeCOA4k9Ql99LCTTFzU-fnf6wyCAKq0g1i5QxFgNNBrZGMbIbFFt96A4WGQBO1J', 'width': 3024}, {'height': 1650, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jmJff323BYeFMIzMLzJmxYwD-2g0EDLrOpGks_FbmyrcYfqnstiZ5U5TUNDGNuC0hN0qN0lw8qjnTZCcPmfJvJH5Rw6AnSuVcWACS45D3o9SVDEFFMg1tfSF1uudbSLT54w63lh0QXj4SqOtYxISaUusPahxCXSHqxa-v8-yhVo_t6B', 'width': 1275}, {'height': 3264, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/117685926906985511601">Mahim Hegde</a>'], 'photo_reference': 'AUjq9jnWZfCKYMFcUXoOBWghItru6bc8lwZF7QSaAECOUu-JJ684azbtplyQcjnLdsr_ZA6ocM-G-JaXsjMVKPjen_KKAWKCj2-OfYIRc_rlm0o4sEePGf2NDpwitGMxnQ8itKHweK3L4CeiJx-Mn71j1gbGiVnXPpRHiYfk_4UQYPwJ9o3i', 'width': 2448}, {'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jngXTtuMCD-Pt2OmZcwEKS40hC5rpC9fKJxnx0-ZVLv4RWNt38JRWcaz6xGPXBUKf9sdhH51EhciXmYfM2hWvgi3qNAJvQ6LALvAuP6y3bChqLSefLhlAwQuq395cuhTCoviwWZAjFCO6lsKjDo0mekdGlc4TpxXx2nJUytXq3d1IgS', 'width': 960}, {'height': 1280, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jlNsDNyP6iGDW5G0IEJRTUasz4LkHXbw6YEIly95wgh6fzUSYaAKTL2csQ8n3toTuhUQIsVy6ekD2ZjUXQIk4FHLLkjI_-mIsQWQWmefjh867qtQprVjyC7Cn38OMdbiHq0M1GlEbZNmACByoLF_cr3jgOMZ0bbqSq8P3ySlE15A9J5', 'width': 1280}, {'height': 1280, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jkPG8gKWMtee3Ct8KGUDlber9BW4PqCySq8LhSOYJmAYltKg4hnV-n0UejRM91RHEiW1CCDph049QiJ_wNNowXEX0Ozj0nMjyu0PhF6o01k52bO8BvoViUlSdfOUCom_ZGTw48oMKMvkrCPSGzQuJadfA-DOWbPuiubtO6ur9t-XeYG', 'width': 1280}, {'height': 500, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jn9GgvLFriqvar95wBBO9C44wSkVPpD7BMd6ArKwebr9Lyjq-93XbVEPvkP-pWWnYBfJ6XkLiM21a_W7mNqzv_JlzGnGCUs-YFJ4ugFzmUVWupb-aSM8EdntR7RjNg_hKyGOeXqu_HUOBdTCT7aVgawoy4P9H_i7UN_lps_fmqAJ8ub', 'width': 500}, {'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jlkN2f5c9x01-8wd6hVFQZRITX0Rar1RgnKeViKewap2DNzMoY_5QFqchKpWyqyJrSNd7X2elYUGhA-G-qNoH3cCrNDeexeHV3lMragck_96Kfj4crDmjVqDQNvl-jaE79PhkzmESSV6iOySH8s9lgIyr8o-T27LlqL5z0taUxPvbRq', 'width': 960}], 'place_id': 'ChIJj3S0t1IbLxgRYgL-7uH0NIo', 'plus_code': {'compound_code': 'PQ36+HM Nairobi, Kenya', 'global_code': '6GCRPQ36+HM'}, 'price_level': 2, 'rating': 4.3, 'reference': 'ChIJj3S0t1IbLxgRYgL-7uH0NIo', 'reservable': True, 'reviews': [{'author_name': 'David Kanagaretnam', 'author_url': 'https://www.google.com/maps/contrib/109567623568041706461/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5R7RaF1ueYKm_U0ye8jTBBG7K5T3fjTBWQ1MO4BiQ=s128-c0x00000000-cc-rp-mo-ba5', 'rating': 5, 'relative_time_description': 'a year ago', 'text': 'This is a great restaurant for Indian foods mainly however, you will get Kenyan and others too. A calm place to dine with your family and its has a big parking space.  Staff are welcoming and serving the food fast. The place is clean. Prices for food is affordable.', 'time': 1649416437, 'translated': False}, {'author_name': 'Julliet Esta', 'author_url': 'https://www.google.com/maps/contrib/109510066687005858247/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5TQOlQJn_hcLNSJJbB7omg4O-RCyfpbt-4t3unXQls=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 5, 'relative_time_description': '11 months ago', 'text': "We received a warm welcome, service was fast, the food was great and the portions are definitely enough. I would recommend this restaurant for Indian, Chinese and African cuisine, there's a large parking area, kids play area and also a kids menu. The food was also affordable", 'time': 1651396718, 'translated': False}, {'author_name': 'Aoko Gathoni', 'author_url': 'https://www.google.com/maps/contrib/110036374557197962895/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5RHO3ZIMXY_WihCLk7C2xcQcTKdoc5-QhSNkoWh=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 4, 'relative_time_description': '4 months ago', 'text': "When I arrived, the place looked like it wasn't open. But upon asking someone there, he said it was open.\nI ordered for the half koroga chicken with Naan, and to drink, I had tea masala. I liked that their portions were good size.\nI would definitely go back there.", 'time': 1670771464, 'translated': False}, {'author_name': 'Duncanah Gwat', 'author_url': 'https://www.google.com/maps/contrib/116990714119709426524/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5QXiXwls4KibppDfJxM5IHebKyTFfNr5J2j_LoEmw=s128-c0x00000000-cc-rp-mo-ba2', 'rating': 5, 'relative_time_description': '2 months ago',
        # 'text': 'Beutiful place to be, went for a late lunch, nicely ushered in, the waiter was very polite, super helpful. The serve was quick too. The meal was tasty as well', 'time': 1675536564, 'translated': False}, {'author_name': 'B -', 'author_url': 'https://www.google.com/maps/contrib/111323236689199522335/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5Rp3yfS6xwFBSbA9ZvQjd0F50zh5RkWTANNhk44IeI=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 1, 'relative_time_description': '2 weeks ago', 'text': 'Lovely place. Quiet and clean. Polite and friendly staff and they make really good Indian food. The parking is a bit cramped but overall a good intimate experience. The prices are also very agreeable.\n\nI went back recently and standards have plummeted. Its now a really horrible, depressing restaurant that has no identity. It wants to be an Indian restaurant but cant, also Chinese but not happening. Poor service and food that was definitely not fresh.', 'time': 1680543330, 'translated': False}], 'serves_beer': True, 'serves_brunch': True, 'serves_dinner': True, 'serves_lunch': True, 'serves_vegetarian_food': True, 'serves_wine': True, 'takeout': True, 'types': ['restaurant', 'food', 'point_of_interest', 'establishment'], 'url': 'https://maps.google.com/?cid=9958853927237452386', 'user_ratings_total': 171, 'utc_offset': 180, 'vicinity': 'kingara Road, opp kingara close behind Junction Mall, Nairobi', 'website': 'https://whitefieldrestaurant.reserveport.com/', 'wheelchair_accessible_entrance': True}, 'status': 'OK'}
        return JsonResponse({"info":"Kindly use a POST request instead of GET"})
    def post(self, request, format=None):
        myDict = request.data
        # myDict = request.data
        latt1 = float(myDict['latt1'].strip())
        lonn1 = float(myDict['lonn1'].strip())
        latt2 = float(myDict['latt2'].strip())
        lonn2= float(myDict['lonn2'].strip())
        distance = dh.get_difference(latt1,lonn1, latt2,lonn2)
        result_dict ={"distance":distance}
        # return JsonResponse()
        return Response(result_dict,status=status.HTTP_200_OK)
class GetCategories(APIView):
    def get(self, request, format=None):
        myDict = request.data
        try:
            wanted_api_key = myDict['api_key']
            print("wanted_api_key ------>>> ", wanted_api_key)
            type_error_message = "Invalid key."
            res = dh.processApikey(wanted_api_key)
            if res.status_code == 400:
                raise ValueError(type_error_message)

            foods = ["Restaurant",    "Cafe",    "Bar",    "Fast food restaurant",    "Food truck",    "Grocery store",    "Farmers market",    "Deli",    "Bakery",    "Ice cream shop",    "Coffee shop",    "Tea shop",    "Wine bar",    "Brewery",    "Distillery",
    "Hotel",    "Motel",    "Bed and breakfast",    "Apartment",    "Vacation rental",    "Hostel",    "Camping ground",    "RV park",    "Inn",    "Guesthouse",    "Retreat",    "Spa resort",    "Timeshare",]
            entertainment = ["Theater",    "Museum",    "Concert hall",    "Art gallery",    "Movie theater",    "Nightclub",    "Bar",    "Comedy club",    "Music venue",    "Performing arts center",    "Dance studio",    "Librarie",    "Zoo",    "Aquarium",    "Theme park",    "Amusement park",    "Water park"]
            health_and_spiritual = ["Business",     "Government office",     "School",    "College and University",          "Clinic",     "Gym",     "Yoga studio",     "Martial arts studio",     "Dance studio",     "Church",     "Mosque",     "Synagogue",     "Temple",     "Community center",     "Chambers of commerce",     "Trade association",     "Professional organization"
    "Hospital",     "Clinic",     "Gym",     "Yoga studio",     "Martial arts studio",     "Dance studio",     "Massage" "therapist",     "Chiropractor",     "Dentist",     "Doctor",     "Optometrist",     "Pharmacy"]
            sports = ["Park",    "Beach",    "Garden",    "Zoo",    "Aquarium",    "Theme park",    "Amusement park",    "Water park",    "Golf course",    "Tennis court",    "Hiking trail",    "Bike path",    "Ski resort",    "Snowboarding resort",    "Beach"
    "volleyball court",   "Basketball court",    "Soccer field",    "Football field"]
            shops = ["Store",    "Mall",    "Outlet mall",    "Grocery store",    "Farmers market",    "Department store",    "Clothing store",    "Shoe store",    "Jewelry store",    "Electronics store",    "Furniture store",    "Home improvement store",    "Sporting good store"]
            transport = ["Airport",    "Bus station",    "Train station",    "Taxi stand",    "Car rental agency",    "Ferry terminal",    "Parking garage",    "Gas station",    "Tow truck company"]
            categories = foods+ entertainment +health_and_spiritual+sports+shops+transport
        # categories = foods
            print("length cats", len(categories))
            categories = list(set(categories))
        # cats = sorted(categories)
            cats = sorted([x.strip().title() for x in categories])
            print("length cats", len(categories))
        # ll = [{"place_id":"EhdQUTM2K0hNLCBOYWlyb2JpLCBLZW55YSImOiQKCg2PPDr_FWtj6RUQChoUChIJp0lN2HIRLxgRTJKXslQCz_c","place_name":"PQ36+HM","category":["street_address"],"address":"PQ36+HM, Nairobi, Kenya","location_coord":"-1.2960625 , 36.7616875","day_hours":"None","phone":"None","website":"None","type_of_data":"scraped","is_test_data":True,"eventId":["FB1010000000000000000000003004"],"error":False}]
        # ll2 = {'html_attributions': [], 'result': {'address_components': [{'long_name': 'Nairobi', 'short_name': 'Nairobi', 'types': ['locality', 'political']}, {'long_name': 'Maziwa', 'short_name': 'Maziwa', 'types': ['sublocality_level_1', 'sublocality', 'political']}, {'long_name': 'Nairobi County', 'short_name': 'Nairobi County', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'Kenya', 'short_name': 'KE', 'types': ['country', 'political']}, {'long_name': '00600', 'short_name': '00600', 'types': ['postal_code']}], 'adr_address': 'kingara Road, <span class="street-address">opp kingara close behind Junction Mall</span>, <span class="postal-code">00600</span>, <span class="locality">Nairobi</span>, <span class="country-name">Kenya</span>', 'business_status': 'OPERATIONAL', 'current_opening_hours': {'open_now': True, 'periods': [{'close': {'date': '2023-04-23', 'day': 0, 'time': '2100'}, 'open': {'date': '2023-04-23', 'day': 0, 'time': '1100'}}, {'close': {'date': '2023-04-24', 'day': 1, 'time': '2100'}, 'open': {'date': '2023-04-24', 'day': 1, 'time': '1100'}}, {'close': {'date': '2023-04-25', 'day': 2, 'time': '2100'}, 'open': {'date': '2023-04-25', 'day': 2, 'time': '1100'}}, {'close': {'date': '2023-04-26', 'day': 3, 'time': '2100'}, 'open': {'date': '2023-04-26', 'day': 3, 'time': '1100'}}, {'close': {'date': '2023-04-27', 'day': 4, 'time': '2100'}, 'open': {'date': '2023-04-27', 'day': 4, 'time': '1100'}}, {'close': {'date': '2023-04-21', 'day': 5, 'time': '2100'}, 'open': {'date': '2023-04-21', 'day': 5, 'time': '1100'}}, {'close': {'date': '2023-04-22', 'day': 6, 'time': '2100'}, 'open': {'date': '2023-04-22', 'day': 6, 'time': '1100'}}], 'weekday_text': ['Monday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Tuesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Wednesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Thursday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Friday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Saturday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Sunday: 11:00\u202fAM\u2009–\u20099:00\u202fPM']}, 'delivery': True, 'dine_in': True, 'formatted_address': 'kingara Road, opp kingara close behind Junction Mall, Nairobi, Kenya', 'formatted_phone_number': '0742 894700', 'geometry': {'location': {'lat': -1.2960063, 'lng': 36.7616708}, 'viewport': {'northeast': {'lat': -1.294604919708498, 'lng': 36.7631173802915}, 'southwest': {'lat': -1.297302880291502, 'lng': 36.76041941970851}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png', 'icon_background_color': '#FF9E67', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet', 'international_phone_number': '+254 742 894700', 'name': 'Whitefield Restaurant', 'opening_hours': {'open_now': True, 'periods': [{'close': {'day': 0, 'time': '2100'}, 'open': {'day': 0, 'time': '1100'}}, {'close': {'day': 1, 'time': '2100'}, 'open': {'day': 1, 'time': '1100'}}, {'close': {'day': 2, 'time': '2100'}, 'open': {'day': 2, 'time': '1100'}}, {'close': {'day': 3, 'time': '2100'}, 'open': {'day': 3, 'time': '1100'}}, {'close': {'day': 4, 'time': '2100'}, 'open': {'day': 4, 'time': '1100'}}, {'close': {'day': 5, 'time': '2100'}, 'open': {'day': 5, 'time': '1100'}}, {'close': {'day': 6, 'time': '2100'}, 'open': {'day': 6, 'time': '1100'}}], 'weekday_text': ['Monday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Tuesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Wednesday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Thursday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Friday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Saturday: 11:00\u202fAM\u2009–\u20099:00\u202fPM', 'Sunday: 11:00\u202fAM\u2009–\u20099:00\u202fPM']}, 'photos': [{'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jkATuC0T8GjDwd36b2qFmdvX05LoynTd7UYt21ecQeWWbhro-dFZ1X5fmPWgnYx3St6-5ceQoznAl9kiFDzRBivsyP_rNHc0jA9vHJ0SZ2wwzamP4FcP2Pu_36nSZObngCkWOcLN3UeLo5meFYAGLaWsxhhiJjlX2QcM64ZL9CP1_bP', 'width': 960}, {'height': 2448, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jnZFX2-uMZTgVBBo52uE6iWjdNFAemLYStnV1LOKq5vrrkdfvLF8UR0VPrYgo9ZzNFPkZusndaGms8EGKdgWpU02jL59Hr-HZy0tgpD13AV1ikVuKAWuxury0aLX5H845y_JoKhcbRhknrAT1tKEpUvnqth6heS34IZvjxEf3YDiXUB', 'width': 3264}, {'height': 4032, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/117873843766263809334">Evans Sigei</a>'], 'photo_reference': 'AUjq9jmoR1PWZKV0rA8iYwS2LqOJJRtntAmFwurFxPNWpm8hQft8wZnDk_RcC-RwLdDv7AxsLTeLrFUNB554gZ2sR1xKR1DJ7DzbjNyGF-aOQh43DMSKMqeCOA4k9Ql99LCTTFzU-fnf6wyCAKq0g1i5QxFgNNBrZGMbIbFFt96A4WGQBO1J', 'width': 3024}, {'height': 1650, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jmJff323BYeFMIzMLzJmxYwD-2g0EDLrOpGks_FbmyrcYfqnstiZ5U5TUNDGNuC0hN0qN0lw8qjnTZCcPmfJvJH5Rw6AnSuVcWACS45D3o9SVDEFFMg1tfSF1uudbSLT54w63lh0QXj4SqOtYxISaUusPahxCXSHqxa-v8-yhVo_t6B', 'width': 1275}, {'height': 3264, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/117685926906985511601">Mahim Hegde</a>'], 'photo_reference': 'AUjq9jnWZfCKYMFcUXoOBWghItru6bc8lwZF7QSaAECOUu-JJ684azbtplyQcjnLdsr_ZA6ocM-G-JaXsjMVKPjen_KKAWKCj2-OfYIRc_rlm0o4sEePGf2NDpwitGMxnQ8itKHweK3L4CeiJx-Mn71j1gbGiVnXPpRHiYfk_4UQYPwJ9o3i', 'width': 2448}, {'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jngXTtuMCD-Pt2OmZcwEKS40hC5rpC9fKJxnx0-ZVLv4RWNt38JRWcaz6xGPXBUKf9sdhH51EhciXmYfM2hWvgi3qNAJvQ6LALvAuP6y3bChqLSefLhlAwQuq395cuhTCoviwWZAjFCO6lsKjDo0mekdGlc4TpxXx2nJUytXq3d1IgS', 'width': 960}, {'height': 1280, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jlNsDNyP6iGDW5G0IEJRTUasz4LkHXbw6YEIly95wgh6fzUSYaAKTL2csQ8n3toTuhUQIsVy6ekD2ZjUXQIk4FHLLkjI_-mIsQWQWmefjh867qtQprVjyC7Cn38OMdbiHq0M1GlEbZNmACByoLF_cr3jgOMZ0bbqSq8P3ySlE15A9J5', 'width': 1280}, {'height': 1280, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jkPG8gKWMtee3Ct8KGUDlber9BW4PqCySq8LhSOYJmAYltKg4hnV-n0UejRM91RHEiW1CCDph049QiJ_wNNowXEX0Ozj0nMjyu0PhF6o01k52bO8BvoViUlSdfOUCom_ZGTw48oMKMvkrCPSGzQuJadfA-DOWbPuiubtO6ur9t-XeYG', 'width': 1280}, {'height': 500, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jn9GgvLFriqvar95wBBO9C44wSkVPpD7BMd6ArKwebr9Lyjq-93XbVEPvkP-pWWnYBfJ6XkLiM21a_W7mNqzv_JlzGnGCUs-YFJ4ugFzmUVWupb-aSM8EdntR7RjNg_hKyGOeXqu_HUOBdTCT7aVgawoy4P9H_i7UN_lps_fmqAJ8ub', 'width': 500}, {'height': 720, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111709173699870817395">Whitefield Restaurant</a>'], 'photo_reference': 'AUjq9jlkN2f5c9x01-8wd6hVFQZRITX0Rar1RgnKeViKewap2DNzMoY_5QFqchKpWyqyJrSNd7X2elYUGhA-G-qNoH3cCrNDeexeHV3lMragck_96Kfj4crDmjVqDQNvl-jaE79PhkzmESSV6iOySH8s9lgIyr8o-T27LlqL5z0taUxPvbRq', 'width': 960}], 'place_id': 'ChIJj3S0t1IbLxgRYgL-7uH0NIo', 'plus_code': {'compound_code': 'PQ36+HM Nairobi, Kenya', 'global_code': '6GCRPQ36+HM'}, 'price_level': 2, 'rating': 4.3, 'reference': 'ChIJj3S0t1IbLxgRYgL-7uH0NIo', 'reservable': True, 'reviews': [{'author_name': 'David Kanagaretnam', 'author_url': 'https://www.google.com/maps/contrib/109567623568041706461/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5R7RaF1ueYKm_U0ye8jTBBG7K5T3fjTBWQ1MO4BiQ=s128-c0x00000000-cc-rp-mo-ba5', 'rating': 5, 'relative_time_description': 'a year ago', 'text': 'This is a great restaurant for Indian foods mainly however, you will get Kenyan and others too. A calm place to dine with your family and its has a big parking space.  Staff are welcoming and serving the food fast. The place is clean. Prices for food is affordable.', 'time': 1649416437, 'translated': False}, {'author_name': 'Julliet Esta', 'author_url': 'https://www.google.com/maps/contrib/109510066687005858247/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5TQOlQJn_hcLNSJJbB7omg4O-RCyfpbt-4t3unXQls=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 5, 'relative_time_description': '11 months ago', 'text': "We received a warm welcome, service was fast, the food was great and the portions are definitely enough. I would recommend this restaurant for Indian, Chinese and African cuisine, there's a large parking area, kids play area and also a kids menu. The food was also affordable", 'time': 1651396718, 'translated': False}, {'author_name': 'Aoko Gathoni', 'author_url': 'https://www.google.com/maps/contrib/110036374557197962895/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5RHO3ZIMXY_WihCLk7C2xcQcTKdoc5-QhSNkoWh=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 4, 'relative_time_description': '4 months ago', 'text': "When I arrived, the place looked like it wasn't open. But upon asking someone there, he said it was open.\nI ordered for the half koroga chicken with Naan, and to drink, I had tea masala. I liked that their portions were good size.\nI would definitely go back there.", 'time': 1670771464, 'translated': False}, {'author_name': 'Duncanah Gwat', 'author_url': 'https://www.google.com/maps/contrib/116990714119709426524/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5QXiXwls4KibppDfJxM5IHebKyTFfNr5J2j_LoEmw=s128-c0x00000000-cc-rp-mo-ba2', 'rating': 5, 'relative_time_description': '2 months ago',
        # 'text': 'Beutiful place to be, went for a late lunch, nicely ushered in, the waiter was very polite, super helpful. The serve was quick too. The meal was tasty as well', 'time': 1675536564, 'translated': False}, {'author_name': 'B -', 'author_url': 'https://www.google.com/maps/contrib/111323236689199522335/reviews', 'language': 'en', 'original_language': 'en', 'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ACB-R5Rp3yfS6xwFBSbA9ZvQjd0F50zh5RkWTANNhk44IeI=s128-c0x00000000-cc-rp-mo-ba4', 'rating': 1, 'relative_time_description': '2 weeks ago', 'text': 'Lovely place. Quiet and clean. Polite and friendly staff and they make really good Indian food. The parking is a bit cramped but overall a good intimate experience. The prices are also very agreeable.\n\nI went back recently and standards have plummeted. Its now a really horrible, depressing restaurant that has no identity. It wants to be an Indian restaurant but cant, also Chinese but not happening. Poor service and food that was definitely not fresh.', 'time': 1680543330, 'translated': False}], 'serves_beer': True, 'serves_brunch': True, 'serves_dinner': True, 'serves_lunch': True, 'serves_vegetarian_food': True, 'serves_wine': True, 'takeout': True, 'types': ['restaurant', 'food', 'point_of_interest', 'establishment'], 'url': 'https://maps.google.com/?cid=9958853927237452386', 'user_ratings_total': 171, 'utc_offset': 180, 'vicinity': 'kingara Road, opp kingara close behind Junction Mall, Nairobi', 'website': 'https://whitefieldrestaurant.reserveport.com/', 'wheelchair_accessible_entrance': True}, 'status': 'OK'}
            return JsonResponse({"categories":cats})
        except ValueError:
            return Response(type_error_message, status=status.HTTP_400_BAD_REQUEST)