from tkinter import CASCADE
from django.db import models
from django.urls import reverse

class Realtime(models.Model):
    rt_trip_id = models.CharField(max_length=100)
    rt_route_id = models.CharField(max_length=100)
    rt_schedule = models.CharField(max_length=100)
    rt_stop_sequence = models.CharField(max_length=100)
    rt_stop_id = models.CharField(max_length=100)

    def __str__(self):
        return self.rt_trip_id

class Agency(models.Model):
    agency_id = models.IntegerField(primary_key=True, unique=False)
    agency_name = models.CharField(max_length=100)
    agency_url = models.CharField(max_length=50)
    agency_timezone = models.CharField(max_length=25)
    agency_lang = models.TextField(max_length=10)
    agency_phone = models.TextField(max_length=10, blank=True)

    class Meta:
        ordering = ('agency_id', 'agency_name')
        verbose_name = 'agency'
        verbose_name_plural = 'agencies'

    def __str__(self):
        return str(self.agency_id)

class Calender(models.Model):
    service_id = models.CharField(primary_key=True, unique=True, max_length=10)
    monday = models.IntegerField()
    tuesday = models.IntegerField()
    wednesday = models.IntegerField()
    thursday = models.IntegerField()
    friday = models.IntegerField()
    saturday = models.IntegerField()
    sunday = models.IntegerField()
    start_date = models.IntegerField()
    end_date = models.IntegerField()

    class Meta:
        ordering = ('service_id', 'start_date')
        verbose_name = 'service'
        verbose_name_plural = 'services'

    def __str__(self):
        return str(self.service_id)

class Calender_Dates(models.Model):
    service_id = models.ForeignKey(Calender, on_delete=models.CASCADE)
    date = models.IntegerField(primary_key=True)
    exception_type = models.IntegerField()

    class Meta:
        ordering = ('date', 'service_id')
        verbose_name = 'date'
        verbose_name_plural = 'dates'

    def __str__(self):
        return str(self.date)

class Stop(models.Model):
    stop_id = models.CharField(primary_key=True, unique=False, max_length=30)
    stop_name = models.CharField(max_length=250)
    stop_lat = models.DecimalField(max_digits=25, decimal_places=13)
    stop_lon = models.DecimalField(max_digits=25, decimal_places=13)

    class Meta:
        ordering = ('stop_id', 'stop_name')
        verbose_name = 'stop'
        verbose_name_plural = 'stops'

    def get_absolute_url(self):
        return reverse('main:stops_by_stoptimes', args=[self.stop_id])

    def __str__(self):
        return str(self.stop_name)

class Route(models.Model):
    route_id = models.CharField(primary_key=True, unique=False, max_length=30)
    agency_id = models.ForeignKey(Agency, on_delete=models.CASCADE)
    route_short_name = models.TextField(max_length=5)
    route_long_name = models.TextField(blank=True, max_length=50)
    route_type = models.IntegerField()

    class Meta:
        ordering = ('route_id', 'route_short_name')
        verbose_name = 'route'
        verbose_name_plural = 'routes'

    def __str__(self):
        return self.route_short_name

class Trip(models.Model):
    trip_id = models.CharField(primary_key=True, unique=False, max_length=30)
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE)
    service_id = models.ForeignKey(Calender, on_delete=models.CASCADE)
    shape_id = models.CharField(max_length=50)
    trip_headsign = models.TextField(blank=True, max_length=100)
    direction_id = models.IntegerField()

    class Meta:
        ordering = ('trip_id', 'trip_headsign')
        verbose_name = 'trip'
        verbose_name_plural = 'trips'

    def __str__(self):
        return str(self.route_id)

class Stop_Time(models.Model):
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE)
    stop_id = models.ForeignKey(Stop, on_delete=models.CASCADE)
    stop_sequence = models.IntegerField()
    stop_headsign = models.TextField(max_length=100)
    pickup_type =  models.IntegerField(primary_key=True)
    dropoff_type =  models.IntegerField()
    shape_dist_traveled = models.DecimalField(max_digits=25, decimal_places=13)

    class Meta:
        ordering = ('stop_id', 'arrival_time')
        verbose_name = 'stop_time'
        verbose_name_plural = 'stop_times'

    def __str__(self):
        return self.stop_headsign