from django.db import models

class PlacesRequest(models.Model):
    mongo_id = models.CharField(max_length=255)
    event_id = models.CharField(max_length=255)
    start_address = models.CharField(max_length=255)
    start_lat_lon = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    query_text = models.CharField(max_length=255)
    radius_distance = models.CharField(max_length=255)

    def __str__(self):
        return str(self.url)

class PlacesResponse(models.Model):
    req_id = models.ForeignKey(PlacesRequest, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    lat_lon = models.CharField(max_length=255)
    start_lat_lon = models.CharField(max_length=255)
    data = models.CharField(max_length=255)
    is_error = models.BooleanField(default=False)
    error = models.CharField(max_length=255)

    def __str__(self):
        return str(self.address)

class RouteRequest(models.Model):
    mongo_id = models.CharField(max_length=255)
    event_id = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    start_location = models.CharField(max_length=255)
    start_lat_lon = models.CharField(max_length=255)

    def __str__(self):
        return str(self.url)

class RouteResponse(models.Model):
    req_id = models.ForeignKey(RouteRequest, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    lat_lon = models.CharField(max_length=255)
    data = models.CharField(max_length=255)
    is_error = models.BooleanField(default=False)
    error = models.CharField(max_length=255)

    def __str__(self):
        return str(self.address)

