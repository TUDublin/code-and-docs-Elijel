from time import sleep
import requests
from django.shortcuts import render, get_object_or_404, redirect
from accounts.forms import CustomUserCreationForm, FavoriteStopForm
from accounts.models import CustomUser, FavoriteStop
from .models import Stop, Stop_Time, Trip, Route
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from datetime import timedelta
from django.db.models.functions import Now
import datetime
from django.db.models import Q
from .tasks import Convert
from django.contrib import messages

#Convert List to Dict
def Convert(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct
    
def allStopTimes(request, stop_id=None):
    now = datetime.datetime.now()
    c_page = None
    stop_time_list = None
    if stop_id:
        c_page = get_object_or_404(Stop, stop_id=stop_id)
        stop_lat = c_page.stop_lat
        stop_lon = c_page.stop_lon
        stop_time_list = Stop_Time.objects.filter(Q(stop_id=c_page, arrival_time__gte=now))
        
        # get api objects
        route_list = list(Route.objects.values_list('route_id', 'route_short_name'))
        trip_lists = list(Trip.objects.values_list('service_id', 'trip_id', 'route_id'))
        stoptimes_servicelist = list(stop_time_list.values_list('stop_sequence','trip_id', 'arrival_time', 'stop_headsign'))
        
        # Add route_short_name to any matching trip_id from stop_times == trip
        for item1 in route_list:
            for i in range(len(trip_lists)):
                if item1[0] == trip_lists[i][2]:
                    trip_lists[i] = trip_lists[i] + (item1[1],)
        
        # Add Service ID to any matching Trip ID from stop_times == trip
        for item1 in trip_lists:
            for i in range(len(stoptimes_servicelist)):
                if item1[1] == stoptimes_servicelist[i][1]:
                    stoptimes_servicelist[i] = stoptimes_servicelist[i] + (item1[0],) + (item1[2],) + (item1[3],)
        
        # Add Api stuff to stop_times_servicelist with matching trip_id + stop_sequence
        converted_list = [list(tup) for tup in stoptimes_servicelist]
        StopTimes_Dict = []
        
        for row in converted_list:
            row.insert(0, 'stop_sequence')
            row.insert(2, 'trip_id')
            row.insert(4, 'arrival_time')
            row.insert(6, 'stop_headsign')
            row.insert(8, 'service_id')
            row.insert(10, 'route_id')
            row.insert(12, 'route_short_name')
            StopTimes_Dict.append(Convert(row))

        #Filter
        keyValList = ['2']
        filteredTimeList = [d for d in StopTimes_Dict if d['service_id'] in keyValList]

    '''Pagination Code'''
    paginator = Paginator(filteredTimeList, 12)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        filteredTimeLists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        filteredTimeLists = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = FavoriteStopForm(request.POST)
        if form.is_valid():
            favorite_stop = form.cleaned_data['stop']
            favorite, created = FavoriteStop.objects.get_or_create(user=request.user, stop=favorite_stop)
            if created:
                messages.success(request, 'Stop added to favorites successfully.')
                return redirect('favoriteStops')
            else:
                messages.warning(request, 'This stop is already in your favorites.')
        else:
            messages.error(request, 'Form is not valid.')
    else:
        form = FavoriteStopForm()
        
    return render(request,'realtime/stoptimes.html',{'stop':c_page, 'stop_time_list':filteredTimeLists, 'stop_lat': stop_lat, 'stop_lon': stop_lon, 'form':form})

    
def allStops(request, stop_id=None):
    c_page = None
    stop_list = None
    if stop_id != None:
        c_page = get_object_or_404(Stop, stop_id=stop_id)
        stop_list = Stop.objects.filter(stop_id=c_page)
    else:
        stop_list = Stop.objects.all().filter()

    '''Pagination Code'''
    paginator = Paginator(stop_list, 100)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        stop_lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        stop_lists = paginator.page(paginator.num_pages)
    return render(request,'realtime/stop.html',{'stops':c_page,'stop_lists':stop_lists})













































def home(request):
    url='https://api.nationaltransport.ie/gtfsr/v1?format=json'

    headers = {
        'X-API-KEY': 'ddece4bcc95b497f97aaa72b96617dca',
        'Content-Type': 'application/json; charset=utf-8',
        'User-agent': 'your bot 0.1'
    }

    response = requests.get(url, headers=headers, verify=True).json()

    realtimedict = []
    for each in range(len(response["Entity"])):
        for items in range(len(response["Entity"][each]["TripUpdate"]["StopTimeUpdate"])):
                    rt_trip_id = (response["Entity"][each]["TripUpdate"]["Trip"]["TripId"]) #TripID
                    rt_route_id = (response["Entity"][each]["TripUpdate"]["Trip"]["RouteId"]) #RouteId
                    rt_schedule = (response["Entity"][each]["TripUpdate"]["Trip"]["ScheduleRelationship"]) #ScheduleRelationship
                    rt_stop_sequence = (response["Entity"][each]["TripUpdate"]["StopTimeUpdate"][items]["StopSequence"]) #StopSequence
                    rt_stop_id = (response["Entity"][each]["TripUpdate"]["StopTimeUpdate"][items]["StopId"]) #StopId
                    realtimedict.append(list({'rt_trip_id': rt_trip_id, 'rt_route_id':rt_route_id, 'rt_schedule':rt_schedule, 'rt_stop_sequence':rt_stop_sequence, 'rt_stop_id':rt_stop_id}))
 
    return render(request,'realtime/test.html',({'response':response, 'result':realtimedict}))
