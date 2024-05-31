from django.shortcuts import render
import requests
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from accounts.data_cube_views_maptracker import insert_data, get_data, delete_data
from api.utils import insert_data, get_data
api_key = "1b834e07-c68b-4bf6-96dd-ab7cdc62f07f"

# --------------------------------------------------------------------------------------------------------
# CLASS ATTENDANCE ENDPOINTS
class ClassAttendanceView(APIView):
    def get(self, request):
        return Response({"data": "Kindly use a POST request instead of GET"}, status=status.HTTP_200_OK)
    
    def post(self, request):
        payload = request.data
        payload.update({"doc_type": "attendance"})

        response = insert_data(api_key, collection="class_attendance", data=payload, payment=False)
        return Response(response, status=status.HTTP_200_OK)
    
class FetchClassAttendanceByClassNameView(APIView):
    def get(self, request):
        return Response({"data": "Kindly use a POST request instead of GET"}, status=status.HTTP_200_OK)
    
    def post(self, request):
        class_name = request.data.get('class_name')
        date = request.data.get('datetime')
        
        if not class_name or not date:
            return Response({"error": "class_name and date are required"}, status=status.HTTP_400_BAD_REQUEST)

        response = get_data(api_key, collection="class_attendance", fil={"class_name": class_name, "datetime": date}, payment=False)
        return Response(response, status=status.HTTP_200_OK)

class FetchClassAttendanceByWorkspaceView(APIView):
    def get(self, request):
        return Response({"data": "Kindly use a POST request instead of GET"}, status=status.HTTP_200_OK)
    
    def post(self, request):
        workspace_id = request.data.get('workspace_id')
        date = request.data.get('datetime')
        
        if not workspace_id or not date:
            return Response({"error": "workspace_id and date are required"}, status=status.HTTP_400_BAD_REQUEST)

        response = get_data(api_key, collection="class_attendance", fil={"workspace_id": workspace_id, "datetime": date}, payment=False)
        return Response(response, status=status.HTTP_200_OK)
    
# --------------------------------------------------------------------------------------------------------
# BUS ATTENDANCE ENDPOINTS
class BusAttendanceView(APIView):
    def get(self, request):
        return Response({"data": "Kindly use a POST request instead of GET"}, status=status.HTTP_200_OK)
    
    def post(self, request):
        payload = request.data
        payload.update({"doc_type": "attendance"})

        response = insert_data(api_key, collection="bus_attendance", data=payload, payment=False)
        return Response(response, status=status.HTTP_200_OK)
    

class FetchBusAttendanceByBusNameView(APIView):
    def get(self, request):
        return Response({"data": "Kindly use a POST request instead of GET"}, status=status.HTTP_200_OK)
    
    def post(self, request):
        bus_name = request.data.get('bus_name')
        date = request.data.get('datetime')
        
        if not bus_name or not date:
            return Response({"error": "bus_name and date are required"}, status=status.HTTP_400_BAD_REQUEST)

        response = get_data(api_key, collection="bus_attendance", fil={"bus_name": bus_name, "datetime": date}, payment=False)
        return Response(response, status=status.HTTP_200_OK)

class FetchBusAttendanceByWorkspaceView(APIView):
    def get(self, request):
        return Response({"data": "Kindly use a POST request instead of GET"}, status=status.HTTP_200_OK)
    
    def post(self, request):
        workspace_id = request.data.get('workspace_id')
        date = request.data.get('datetime')
        
        if not workspace_id or not date:
            return Response({"error": "workspace_id and date are required"}, status=status.HTTP_400_BAD_REQUEST)

        response = get_data(api_key, collection="bus_attendance", fil={"workspace_id": workspace_id, "datetime": date}, payment=False)
        return Response(response, status=status.HTTP_200_OK)
