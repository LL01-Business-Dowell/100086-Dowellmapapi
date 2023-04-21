from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from accounts import views

urlpatterns = [
    path('get-details/',views.GetPlaceDetails.as_view()),
    path('get-details-list/',views.GetPlaceDetailsList.as_view()),

    #     path('', views.home),
    #     path('home/', views.api, name='home'),

    #     path('api/',views.api, name='api'),

    # path('continents/<slug:username>/<slug:sessionId>/<slug:projectCode>/', views.ContinentList.as_view()),
    # path('countries/<slug:username>/<slug:sessionId>/<slug:projectCode>/', views.CountryList.as_view()),
]