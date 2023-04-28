import requests
from django.shortcuts import render, get_object_or_404
from .models import Stop, Stop_Time, Trip, Route
from django.core.paginator import Paginator, EmptyPage, InvalidPage
import datetime
from django.db.models import Q
from django.shortcuts import render


def allStopTimes(request, stop_id=None):
    now = datetime.datetime.now()
    c_page = None
    stop_time_list = None
    if stop_id:
        c_page = get_object_or_404(Stop, stop_id=stop_id)
        stop_lat = c_page.stop_lat
        stop_lon = c_page.stop_lon
        
        # use select_related to reduce database queries
        stop_time_list = Stop_Time.objects.filter(
            Q(stop_id=c_page),
            Q(arrival_time__gte=now) | Q(departure_time__gte=now)
        ).select_related('trip_id__route_id', 'trip_id__service_id')
        
        # create a list of dictionaries containing all stop times
        stop_times = []
        for st in stop_time_list:
            # check if the arrival or departure time is due now
            if st.arrival_time == now or st.departure_time == now:
                due_now = True
            else:
                due_now = False
                
            stop_times.append({
                'stop_sequence': st.stop_sequence,
                'trip_id': st.trip_id.trip_id,
                'arrival_time': st.arrival_time,
                'departure_time': st.departure_time,
                'stop_headsign': st.stop_headsign,
                'service_id': st.trip_id.service_id.service_id,
                'route_id': st.trip_id.route_id.route_id,
                'route_short_name': st.trip_id.route_id.route_short_name,
                'due_now': due_now  # add a 'due_now' flag to the dictionary
            })
        
        # filter stop times by service_id
        keyValList = ['2']
        filteredTimeList = [st for st in stop_times if st['service_id'] in keyValList]
        
        # paginate the stop times
        paginator = Paginator(filteredTimeList, 12)
        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1
        try:
            filteredTimeLists = paginator.page(page)
        except (EmptyPage, InvalidPage):
            filteredTimeLists = paginator.page(paginator.num_pages)
        
        return render(request, 'Stops/stoptimes.html', {'stop': c_page, 'stop_time_list': filteredTimeLists, 'stop_lat': stop_lat, 'stop_lon': stop_lon})

def allStops(request, stop_id=None):
    c_page = None
    stop_list = None
    if stop_id != None:
        c_page = get_object_or_404(Stop, stop_id=stop_id)
        stop_list = Stop.objects.filter(stop_id=c_page)
    else:
        stop_list = Stop.objects.all().filter()

    if request.GET.get('q'):
        query = request.GET['q']
        stop_list = Stop.objects.filter(Q(stop_name__icontains=query) | Q(stop_id__icontains=query))
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
    return render(request,'Stops/stop.html',{'stops':c_page,'stop_lists':stop_lists})

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
    return render(request,'NearbyStops/nearby_stops.html',{'stops':c_page,'stop_lists':stop_lists})

def home(request):
    return render(request, 'Home/home.html')

def allRoutes(request):
    today = datetime.datetime.today().weekday()

    if today < 5: 
        routes = Route.objects.filter(route_id__icontains='b')
    else:  
        routes = Route.objects.filter(route_id__icontains='d')
    
    search_query = request.GET.get('search')

    if search_query:
        routes = routes.filter(route_id__icontains=search_query)

    routes_per_page = 21
    paginator = Paginator(routes, routes_per_page)
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'Route/route_list.html', context)


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

    return render(request, 'Route/route_detail.html', context)

def destinationsearch(request):
    return render(request, 'Destination/search.html')

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
                return render(request, 'Destination/search.html', {'error_message': f"No stop found with name '{stop_name}'"})
            stop_id = stop.stop_id
            
        today = datetime.datetime.today().weekday()

        trips = Trip.objects.filter(stop_time__stop_id=stop_id)

        if today < 5:  # Monday to Friday
            routes = Route.objects.filter(trip__in=trips,route_id__icontains='d').distinct()
        else:  # Saturday or Sunday
            routes = Route.objects.filter(trip__in=trips,route_id__icontains='b').distinct()

        return render(request, 'Destination/search_results.html', {'routes': routes})
    else:
        return render(request, 'Destination/search.html')












































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
 
    return render(request,'Base/test.html',({'response':response, 'result':realtimedict}))
