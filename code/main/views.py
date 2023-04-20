import requests
from django.shortcuts import render, get_object_or_404
from .models import Stop, Stop_Time, Trip, Route
from django.core.paginator import Paginator, EmptyPage, InvalidPage
import datetime
from django.db.models import Q
from .tasks import Convert
from django.shortcuts import render
from .models import Stop, Stop_Time

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
        
    return render(request,'realtime/stoptimes.html',{'stop':c_page, 'stop_time_list':filteredTimeLists, 'stop_lat': stop_lat, 'stop_lon': stop_lon})

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

def nearby_stops(request, stop_id=None):
    c_page = None
    stop_list = None
    if stop_id != None:
        c_page = get_object_or_404(Stop, stop_id=stop_id)
        stop_list = Stop.objects.filter(stop_id=c_page)
    else:
        stop_list = Stop.objects.all().filter()

    '''Pagination Code'''
    paginator = Paginator(stop_list, 4349)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        stop_lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        stop_lists = paginator.page(paginator.num_pages)
    return render(request,'realtime/nearby_stops.html',{'stops':c_page,'stop_lists':stop_lists})

def home(request):
    return render(request, 'realtime/home.html')

from django.shortcuts import render
from .models import Route, Stop, Trip


import datetime

from django.core.paginator import Paginator

def allRoutes(request):
    # Get the current day of the week
    today = datetime.datetime.today().weekday()

    if today < 5:  # Monday to Friday
        routes = Route.objects.filter(route_id__icontains='b')
    else:  # Saturday or Sunday
        routes = Route.objects.filter(route_id__icontains='d')
    
    # Number of routes to display per page
    routes_per_page = 21

    # Create the Paginator object
    paginator = Paginator(routes, routes_per_page)

    # Get the current page number from the query parameters
    page_number = request.GET.get('page')

    # Get the current page of routes
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'realtime/route_list.html', context)


def routeDetails(request, route_id):
    # Get all the trips associated with the Route object
    trips = Trip.objects.filter(route_id=route_id)

    # Check if the form was submitted with a shape filter
    shape_filter = request.POST.get('shape_filter', 'O')
    if shape_filter:
        trips = trips.filter(shape_id__icontains=shape_filter)

    # Get all the stops associated with the trips
    stops = Stop.objects.filter(stop_time__trip_id__in=trips).distinct().order_by('stop_time__stop_sequence')


    locations = Stop.objects.filter(stop_time__trip_id__in=trips).distinct()

    # Paginate stops
    paginator = Paginator(stops, 13)
    page = request.GET.get('page')
    stops = paginator.get_page(page)

    # Store the headsigns in a dictionary
    headsigns = {
        'I': None,
        'O': None
    }

    for trip in trips:
        if trip.shape_id:
            if trip.shape_id.__contains__('O'):
                headsigns['O'] = 'Change Direction'
            elif trip.shape_id.__contains__('I'):
                headsigns['I'] = 'Change Direction'

    # Store the stops and headsigns in the dictionary with the route as the key
    context = {
        'trips': trips,
        'stops': stops,
        'headsigns': headsigns,
        'locations' : locations
    }

    return render(request, 'realtime/route_detail.html', context)

def destinationsearch(request):
    return render(request, 'realtime/search.html')

def destination(request):
    if request.method == 'GET':
        search_term = request.GET.get('search_term')
        search_type = request.GET.get('search_type')

        if search_type == 'stop_id':
            stop_id = search_term
        else:
            stop_name = search_term
            stop = Stop.objects.filter(stop_name__icontains=stop_name).first()
            if stop is None:
                return render(request, 'realtime/search.html', {'error_message': f"No stop found with name '{stop_name}'"})
            stop_id = stop.stop_id
            
        today = datetime.datetime.today().weekday()

        trips = Trip.objects.filter(stop_time__stop_id=stop_id)

        if today < 5:  # Monday to Friday
            routes = Route.objects.filter(trip__in=trips,route_id__icontains='d').distinct()
        else:  # Saturday or Sunday
            routes = Route.objects.filter(trip__in=trips,route_id__icontains='b').distinct()

        return render(request, 'realtime/search_results.html', {'routes': routes})
    else:
        return render(request, 'realtime/search.html')












































def test(request):
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
