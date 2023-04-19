from django.shortcuts import render
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json
# Create your views here.
class CustomError(Exception):
    pass
class GetPlaceDetails(APIView):
    """
    List all countries, or create a new country.
    """
    def get(self, request, format=None):
        return JsonResponse({"status":"All good"})
#         status_dict = dict()
#         # countries = Countries.objects.all()
#         # serializer = CountrySerializer(countries, many=True)        
#         # status_dict["isSuccess"]=False
#         # countries/<slug:username>/<slug:sessionId>/<slug:projectCode>/
#         req_dict = {}
#         req_dict["request"]="country-list-request"
#         payload = {}
#         payload["username"]=kwargs['username']
#         payload["sessionId"]=kwargs['sessionId']
#         payload["projectCode"]=kwargs['projectCode']
#         req_dict["payload"]=str(payload)
#         status_dict['req'] = str(req_dict)
# ##################
#         status_dict['url'] = "countries/username/sessionId/projectCode/"
#         status_dict['username'] = kwargs['username']
#         status_dict['session_id'] = kwargs['sessionId']
#         status_dict['project-code'] = kwargs['projectCode']

#         try:
#             bad_id_list = [14,8,9,11,13,10,63, 64,16, 15]
#             countries = Countries.objects.all().exclude(id__in=bad_id_list)
#             serializer = CountrySerializer(countries, many=True)
#             status_dict["isSuccess"]=True
#             status_dict["isError"]=False
#             # status_dict["continents"]="Successful"
#             status_dict['response'] = status.HTTP_200_OK
#             record_re(status_dict)

#             return Response(serializer.data)
#         except CustomError:
#             status_dict["isSuccess"]=False
#             status_dict["isError"]=True
#             # status_dict["continents"]="Successful"
#             status_dict['response'] = status.HTTP_400_BAD_REQUEST
#             record_re(status_dict)

#             return Response("Wrong query type '"+kwargs['query_type']+"'", status=status.HTTP_400_BAD_REQUEST)
#         except Http404:
#             status_dict["isSuccess"]=False
#             status_dict["isError"]=True
#             # status_dict["continents"]="Successful"
#             status_dict['response'] = status.HTTP_400_BAD_REQUEST
#             record_re(status_dict)

#             return Response("'"+ kwargs['query_value']+"' not in database", status=status.HTTP_400_BAD_REQUEST)

#         # return Response(serializer.data)

    def post(self, request):
        place_id = request.data.get('place_id')
        url='https://maps.googleapis.com/maps/api/place/details/json?placeid='+place_id+'&key=AIzaSyC_oMIdGvpBALKg6W6TPgpwVLb-viGwonY'
        
        
        try:
            # api_response = api_instance.send_transac_email(send_smtp_email)
            r=requests.get(url)
            print(r.text)
            results = json.loads(r.text)
            print("Type resultsa")
            print(type(results))

            api_response_dict = {"res":results}
            # api_response_dict = api_response.to_dict()
            # print("---The mail has been sent ! Happy :D---")
            return Response(results,status=status.HTTP_200_OK)
        except CustomError:
            # status_dict["isSuccess"]=False
            # status_dict["isError"]=True
            # # status_dict["continents"]="Successful"
            # status_dict['response'] = status.HTTP_400_BAD_REQUEST
            # record_re(status_dict)

            return Response("No results for the place id: "+"place_id", status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            # status_dict["isSuccess"]=False
            # status_dict["isError"]=True
            # # status_dict["continents"]="Successful"
            # status_dict['response'] = status.HTTP_400_BAD_REQUEST
            # record_re(status_dict)

            return Response("No results for the place id: "+"place_id", status=status.HTTP_400_BAD_REQUEST)

        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
