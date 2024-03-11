from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from accounts import views
from accounts import data_cube_views
from accounts import data_cube_views_maptracker
from accounts import health_check_views
urlpatterns = [
    path('get-details/', views.GetPlaceDetails.as_view()),
    path('get-details-list/', views.GetPlaceDetailsList.as_view()),
    path('get-details-list-stage1/', views.GetPlaceDetailsListStage1.as_view()),
    path('save-places-detail/', views.SavePlacesDetail.as_view()),
    path('verify-place-ids/', views.VerifyPlaceIds.as_view()),
    path('get-local-nearby/', views.GetNearbyPlacesLocally.as_view()),
    path('get-local-nearby-v2/', views.GetNearbyPlacesLocallyV2.as_view()),
    path('refresh-json-dh/', views.refresh_json_dh, name='refresh-json-dh'),
    path('show-mongo-data/', views.show_mongo_data, name='show-mongo-data'),
    path('show-json-data/', views.show_json_data, name='show-json-data'),
    path('get-hav-distance/', views.TestLocalDistance.as_view()),
    path('get-categories/', views.GetCategories.as_view()),
    path('get-locs/', data_cube_views.GetLocations.as_view()),
    path('create-profile/', data_cube_views.CreateUserProfile.as_view()),
    path('create-loc-group/', data_cube_views.CreateLocGroup.as_view()),
    path('create-location/', data_cube_views.CreateLocation.as_view()),
    path('update-loc-group/', data_cube_views.UpdateLocGroup.as_view()),
    path('update-location/', data_cube_views.UpdateLocation.as_view()),
    path('delete-user-locs/', data_cube_views.DeleteUserProfile.as_view()),
    path('delete-loc-group/', data_cube_views.DeleteLocGroup.as_view()),
    path('delete-loc/', data_cube_views.DeleteLocation.as_view()),
    path('sync-groups/', data_cube_views.SyncGroups.as_view()),
    # Map tracker
    path('create-workspace/', data_cube_views_maptracker.CreateWorkspace.as_view()),
    path('get-workspace/', data_cube_views_maptracker.GetWorkspace.as_view()),
    path('update-workspace/', data_cube_views_maptracker.UpdateWorkspace.as_view()),
    path('delete-workspace/', data_cube_views_maptracker.DeleteWorkspace.as_view()),
    path('create-current-loc/', data_cube_views_maptracker.CreateLocationData.as_view()),
    path('get-current-loc/', data_cube_views_maptracker.GetLocationData.as_view()),
    path('update-current-loc/', data_cube_views_maptracker.UpdateLocation.as_view()),
    path('delete-current-loc/', data_cube_views_maptracker.DeleteLocationData.as_view()),





    #     path('', views.home),
    #     path('home/', views.api, name='home'),

    #     path('api/',views.api, name='api'),

    # path('continents/<slug:username>/<slug:sessionId>/<slug:projectCode>/', views.ContinentList.as_view()),
    # path('countries/<slug:username>/<slug:sessionId>/<slug:projectCode>/', views.CountryList.as_view()),
    # health_check
    path('health-check/', health_check_views.HealthCheck.as_view(),
         name='health-check'),

]
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
