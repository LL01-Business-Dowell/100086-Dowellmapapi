from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from accounts import views

urlpatterns = [
    path('get-details/',views.GetPlaceDetails.as_view()),
    path('get-details-list/',views.GetPlaceDetailsList.as_view()),
    path('get-details-list-stage1/',views.GetPlaceDetailsListStage1.as_view()),
    path('save-places-detail/',views.SavePlacesDetail.as_view()),
    path('verify-place-ids/',views.VerifyPlaceIds.as_view()),
    path('get-local-nearby/',views.GetNearbyPlacesLocally.as_view()),

    path('refresh-json-dh/',views.refresh_json_dh, name='refresh-json-dh'),
    path('show-mongo-data/',views.show_mongo_data, name='show-mongo-data'),
    path('show-json-data/',views.show_json_data, name='show-json-data'),
    path('get-hav-distance/',views.TestLocalDistance.as_view()),
    #     path('', views.home),
    #     path('home/', views.api, name='home'),

    #     path('api/',views.api, name='api'),

    # path('continents/<slug:username>/<slug:sessionId>/<slug:projectCode>/', views.ContinentList.as_view()),
    # path('countries/<slug:username>/<slug:sessionId>/<slug:projectCode>/', views.CountryList.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])