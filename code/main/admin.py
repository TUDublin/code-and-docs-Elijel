from django.contrib import admin
from .models import Stop, Stop_Time, Route, Trip, Agency, Calender, Calender_Dates, Realtime

admin.site.register(Realtime)

class AgencyAdmin(admin.ModelAdmin):
    list_display = ['agency_id','agency_name','agency_url','agency_timezone','agency_lang','agency_phone']
admin.site.register(Agency, AgencyAdmin)

class CalenderAdmin(admin.ModelAdmin):
    list_display = ['service_id','monday','tuesday','wednesday','thursday','friday','saturday','sunday','start_date','end_date']
admin.site.register(Calender, CalenderAdmin)

class Calender_DatesAdmin(admin.ModelAdmin):
    list_display = ['service_id','date','exception_type']
admin.site.register(Calender_Dates, Calender_DatesAdmin)

class StopAdmin(admin.ModelAdmin):
    list_display = ['stop_id', 'stop_name', 'stop_lat', 'stop_lon']
admin.site.register(Stop, StopAdmin)

class RouteAdmin(admin.ModelAdmin):
    list_display = ['route_id', 'agency_id', 'route_short_name', 'route_long_name', 'route_type']
admin.site.register(Route, RouteAdmin)

class TripAdmin(admin.ModelAdmin):
    list_display = ['route_id', 'service_id', 'trip_id', 'shape_id', 'trip_headsign', 'direction_id']
    list_per_page = 20
admin.site.register(Trip, TripAdmin)

class Stop_TimesAdmin(admin.ModelAdmin):
    list_display = ['arrival_time', 'departure_time', 'trip_id', 'stop_id', 'stop_sequence', 'stop_headsign', 'pickup_type', 'dropoff_type', 'shape_dist_traveled']
    list_per_page = 20
admin.site.register(Stop_Time, Stop_TimesAdmin)