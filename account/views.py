import json
import requests
from django.http import HttpResponse
# from service.datacube import datacube_data_update ,datacube_data_retrieval, datacube_data_delete, datacube_data_insertion, datacube_create_collection
from service.datacube import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserAuthSerializer, UserUpdateSerializer
from .jwt_utils import JWTUtils
from .decorators import login_required
from .helper import *



jwt_utils = JWTUtils()

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@method_decorator(csrf_exempt, name='dispatch')
class UserManagement(APIView):
    def post(self, request):
        type = request.GET.get('type')
        if type == 'get_access_token':
            return self.get_access_token(request)
        elif type == 'update_profile':
            return self.update_userprofile(request)
        elif type == 'authenticate_user':
            return self.authenticate_user(request)

    def get_access_token(self, request):
        refresh_token = request.COOKIES.get('refresh_token') or request.headers.get('Authorization', '').replace(
            'Bearer ', '') or request.data.get('refresh_token')

        if not refresh_token:
            return Response({
                "success": False,
                "message": "Refresh token not provided"
            }, status=status.HTTP_401_UNAUTHORIZED)

        decoded_payload = jwt_utils.decode_jwt_token(refresh_token)
        if not decoded_payload:
            return Response({
                "success": False,
                "message": "Refresh token expired"
            }, status=status.HTTP_401_UNAUTHORIZED)
        user_response = json.loads(datacube_data_retrieval(api_key, "63f3173b44719d743f213102_dowell_survey_database", "voc_user_management", {"_id": decoded_payload["_id"]}, 0, 0, False))

        if not user_response['success']:
            return Response({
                "success": False,
                "message": "User not found"
            }, status=status.HTTP_401_UNAUTHORIZED)

        token = jwt_utils.generate_jwt_tokens(
            user_response['data'][0]['_id'],
            user_response['data'][0]['workspace_id'],
            user_response['data'][0]['portfolio']
        )
        return Response({
            "success": True,
            "message": "Access token generated successfully",
            "access_token": token["access_token"],
            "refresh_token": token["refresh_token"],
            "response": user_response['data'][0]
        })

    def authenticate_user(self, request):
        workspace_name = request.data.get("workspace_name")
        portfolio = request.data.get("portfolio")
        password = request.data.get("password")
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")

        serializer = UserAuthSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Posting wrong data to API",
                "errors": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        client_admin_login_response = dowell_login(workspace_name, portfolio, password)

        # return Response(client_admin_login_response)
        if not client_admin_login_response.get("success") or client_admin_login_response.get("response") == 0:
            return Response({
                "success": False,
                "message": client_admin_login_response.get("message", "Authentication failed")
            }, status=status.HTTP_401_UNAUTHORIZED)

        data = client_admin_login_response.get("response", {})
        user_info = {
            "workspace_name": workspace_name,
            "portfolio": portfolio
        }

        existing_user_response = json.loads(datacube_data_retrieval(api_key, "63f3173b44719d743f213102_dowell_survey_database", "voc_user_management", user_info, 10000, 0, False))
        existing_user = existing_user_response.get('data', [])

        if not existing_user:
            create_user_response = json.loads(datacube_data_insertion(api_key, "63f3173b44719d743f213102_dowell_survey_database", "voc_user_management",
                {
                    **user_info,
                    "email": "",
                    "profile_image": "",
                    "workspace_id": data["userinfo"]["owner_id"],
                    "workspace_owner_name": data["userinfo"]["owner_name"],
                    "portfolio_username": data["portfolio_info"]["username"][0],
                    "member_type": data["portfolio_info"]["member_type"],
                    "data_type": data["portfolio_info"]["data_type"],
                    "operations_right": data["portfolio_info"]["operations_right"],
                    "status": data["portfolio_info"]["status"]
                }
            ))

            if not create_user_response.get("success"):
                return Response({
                    "success": False,
                    "message": "Error while creating user",
                }, status=status.HTTP_400_BAD_REQUEST)

            data = {
                "_id": create_user_response["data"]["inserted_id"],
                **user_info,
                "email": "",
                "profile_image": "",
                "workspace_id": data["userinfo"]["owner_id"],
                "workspace_owner_name": data["userinfo"]["owner_name"],
                "portfolio_username": data["portfolio_info"]["username"][0],
                "member_type": data["portfolio_info"]["member_type"],
                "data_type": data["portfolio_info"]["data_type"],
                "operations_right": data["portfolio_info"]["operations_right"],
                "status": data["portfolio_info"]["status"]
            }

            message = "User created successfully"
        else:
            existing_user_data = existing_user[0]
            data = {
                "_id": existing_user_data["_id"],
                **user_info,
                "email": existing_user_data["email"],
                "profile_image": existing_user_data["profile_image"],
                "workspace_id": existing_user_data["workspace_id"],
                "workspace_owner_name": existing_user_data["workspace_owner_name"],
                "portfolio_username": existing_user_data["portfolio_username"],
                "member_type": existing_user_data["member_type"],
                "data_type": existing_user_data["data_type"],
                "operations_right": existing_user_data["operations_right"],
                "status": existing_user_data["status"]
            }

            message = "User authenticated successfully"
        print(latitude, longitude, data["workspace_id"])
        if latitude and longitude:
            try:
                response_location = json.loads(save_location_data(
                    workspaceId=data["workspace_id"],
                    latitude=latitude,
                    longitude=longitude,
                    userId=data["portfolio_username"],
                    event="login"
                ))
                print(response_location)
            except Exception as e:
                print(f"Location save failed: {e}")

                pass

        token = jwt_utils.generate_jwt_tokens(data)
        return Response({
            "success": True,
            "message": message,
            "access_token": token["access_token"],
            "refresh_token": token["refresh_token"],
            "response": data
        })

    @login_required
    def update_userprofile(self, request):
        _id = request.data.get("_id")

        existing_user_response = json.loads(datacube_data_retrieval(api_key, "63f3173b44719d743f213102_dowell_survey_database", "voc_user_management", {"_id": _id}, 10000, 0, False))
        existing_user = existing_user_response.get('data', [])

        if existing_user:
            existing_user_data = existing_user[0]

            recent_data = request.data["data"]

            if recent_data:
                update_serializer = UserUpdateSerializer(data=recent_data)
                if not update_serializer.is_valid():
                    return Response({
                        "success": False,
                        "message": "Posting wrong data to API",
                        "errors": update_serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST)

                email = update_serializer.validated_data.get("email", None)
                profile_image = update_serializer.validated_data.get("profile_image", None)

                updated_data = {

                    "email": email,
                    "profile_image": profile_image
                }

                user_update = json.loads(datacube_data_update(
                    api_key,
                    "63f3173b44719d743f213102_dowell_survey_database",
                    "voc_user_management",
                    {"_id": _id},
                    updated_data
                ))

                message = user_update.get("message")
                return Response({
                    "success": True,
                    "message": message
                }, status=status.HTTP_204_NO_CONTENT)
            else:
                data = {
                    "_id": existing_user_data["_id"],
                    "email": existing_user_data["email"],
                    "profile_image": existing_user_data["profile_image"],
                    "workspace_id": existing_user_data["workspace_id"],
                    "workspace_owner_name": existing_user_data["workspace_owner_name"],
                    "portfolio_username": existing_user_data["portfolio_username"],
                    "member_type": existing_user_data["member_type"],
                    "data_type": existing_user_data["data_type"],
                    "operations_right": existing_user_data["operations_right"],
                    "status": existing_user_data["status"]
                }

                message = "Nothing to update"
                return Response({
                    "success": True,
                    "message": message,
                    "response": data
                })


        else:
            return Response({
                "success": False,
                "message": "User does not exist"
            }, status=status.HTTP_400_BAD_REQUEST)

    def handle_error(self, request):
        return Response({
            "success": False,
            "message": "Invalid request type"
        }, status=status.HTTP_400_BAD_REQUEST)


class KioskAPIView(APIView):
    def post(self, request):
        type = request.GET.get('type')
        if type == 'get_Kiosk_details':
            return self.get_Kiosk_details(request)
        elif type == 'create_Kiosk_details':
            return self.create_Kiosk_details(request)
        elif type == 'update_Kiosk_details':
            return self.update_Kiosk_details(request)
        elif type == 'delete_Kiosk_details':
            return self.delete_Kiosk_details(request)
        else:
            return Response({
                "success": False,
                "message": "Invalid request type"
            }, status=status.HTTP_400_BAD_REQUEST)

    @login_required
    def get_Kiosk_details(self, request):
        _id = request.data.get("_id")
        existing_kiosk_response = json.loads(
            datacube_data_retrieval(api_key, "63f3173b44719d743f213102_dowell_survey_database", "voc_kiosk_management",
                                    {"_id": _id}, 10000, 0, False))
        if existing_kiosk_response:
            return Response({
                "success": True,
                "data": existing_kiosk_response["data"]
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "message": "User does not exist"
            }, status=status.HTTP_400_BAD_REQUEST)

    @login_required
    def create_Kiosk_details(self, request):
        user_id = request.data.get("user_id")
        name = request.data.get("name")
        kiosk_id = request.data.get("kiosk_id")
        date_time = request.data.get("date_time")
        _status = request.data.get("status")
        details = request.data.get("details")
        portfolio_username = request.data.get("portfolio_username")
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")

        create_kiosk_response = json.loads(
            datacube_data_insertion(api_key, "63f3173b44719d743f213102_dowell_survey_database", "voc_kiosk_management",
                                    {
                                        "user_id": user_id,
                                        "name": name,
                                        "portfolio_username": portfolio_username,
                                        "date_time": date_time,
                                        "status": _status,
                                        "details": details,
                                        "latitude":latitude,
                                        "longitude":longitude
                                    }
                                    ))
        if not create_kiosk_response.get("success"):
            return Response({
                "success": False,
                "message": "Error while creating kiosk",
            }, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "_id": create_kiosk_response["data"]["inserted_id"],
            "user_id": user_id,
            "portfolio_username":portfolio_username,
            "name": name,
            "date_time": date_time,
            "status": _status,
            "details": details,
            "latitude": latitude,
            "longitude": longitude
        }


        kiosk_qrcode_image = generate_qr_code(data, portfolio_name=portfolio_username)
        kiosk_qrcode_file_name = generate_file_name(prefix='kiosk_qrcode', extension='png')
        kiosk_qrcode_image_url = upload_qr_code_image(kiosk_qrcode_image, kiosk_qrcode_file_name)
        data["qrcode_image_url"] = kiosk_qrcode_image_url
        return Response({
            "success": True,
            "message": "creating kiosk successfully",
            "data": data
        }, status=status.HTTP_200_OK)

    @login_required
    def update_Kiosk_details(self, request):
        _id = request.data.get("_id")
        update_data = request.data.dict()
        update_kiosk_response = json.loads(
            datacube_data_update(api_key, "63f3173b44719d743f213102_dowell_survey_database", "voc_kiosk_management",
                                 {"_id": _id}, update_data))
        if update_kiosk_response.get("success"):
            return Response({
                "success": True,
                "message": "Kiosk details updated successfully",
                "data": update_data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "message": "Error updating kiosk details"
            }, status=status.HTTP_400_BAD_REQUEST)

    @login_required
    def delete_Kiosk_details(self, request):
        _id = request.data.get("_id")
        delete_kiosk_response = json.loads(
            datacube_data_delete(api_key, "63f3173b44719d743f213102_dowell_survey_database", "voc_kiosk_management",
                                   {"_id": _id}))
        if delete_kiosk_response.get("success"):
            return Response({
                "success": True,
                "message": "Kiosk deleted successfully"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "message": "Error deleting kiosk"
            }, status=status.HTTP_400_BAD_REQUEST)



