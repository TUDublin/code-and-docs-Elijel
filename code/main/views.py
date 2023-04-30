import requests
from django.shortcuts import render, get_object_or_404
from .models import Stop, Stop_Time, Trip, Route
from django.core.paginator import Paginator, EmptyPage, InvalidPage
import datetime
from django.db.models import Q

def allStopTimes(request, stop_id=None):
    now = datetime.datetime.now()
    c_page = None
    stop_time_list = None
    if stop_id:
        c_page = get_object_or_404(Stop, stop_id=stop_id)
        stop_lat = c_page.stop_lat
        stop_lon = c_page.stop_lon
        
        stop_time_list = Stop_Time.objects.filter(
            Q(stop_id=c_page),
            Q(arrival_time__gte=now) | Q(departure_time__gte=now)
        ).select_related('trip_id__route_id', 'trip_id__service_id')
        
        stop_times = []
        for st in stop_time_list:
            now_hm = now.strftime('%H:%M')
            arrival_hm = st.arrival_time.strftime('%H:%M')
            departure_hm = st.departure_time.strftime('%H:%M')
            if arrival_hm == now_hm or departure_hm == now_hm or \
            (now_hm == arrival_hm[:-3] and int(arrival_hm[-2:]) - int(now_hm[-2:]) == 1) or \
            (now_hm == departure_hm[:-3] and int(departure_hm[-2:]) - int(now_hm[-2:]) == 1):
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
                'due_now': due_now
            })
            
        keyValList = ['2']
        filteredTimeList = [st for st in stop_times if st['service_id'] in keyValList]
        
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
    trips = Trip.objects.filter(route_id=route_id)

    shape_filter = request.POST.get('shape_filter', 'O')
    if shape_filter:
        trips = trips.filter(shape_id__icontains=shape_filter)

    stops = Stop.objects.filter(stop_time__trip_id__in=trips).distinct().order_by('stop_time__stop_sequence')

    locations = Stop.objects.filter(stop_time__trip_id__in=trips).distinct()

    paginator = Paginator(stops, 13)
    page = request.GET.get('page')
    stops = paginator.get_page(page)

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






#Depriciated and Stopped Working.
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

# from google.protobuf.json_format import MessageToJson
# from google.transit import gtfs_realtime_pb2

#Attempt at trying to use the new feed
#def protobuf_to_dict(feed):
#    """Converts a GTFS Realtime feed in protocol buffer format to a dictionary."""
#    feed_dict = MessageToJson(feed, preserving_proto_field_name=True)
#   feed_dict = json.loads(feed_dict)
#    return feed_dict

#Attempt at trying to use the new feed
#def stop_details(request, stop_id):
#    url = 'https://api.nationaltransport.ie/gtfsr/v2/gtfsr'
#    api_key = 'd420a4108eed4bdba373ab30581679c9'

#    headers = {'x-api-key': api_key}
#    response = requests.get(url, headers=headers)

#   feed = gtfs_realtime_pb2.FeedMessage()
#    feed.ParseFromString(response.content)
#    feed_dict = protobuf_to_dict(feed)

#    stop_times = []
#    if isinstance(feed.entity, list):
#        entities = feed.entity
#    else:
#        entities = [feed.entity]
#    for entity in entities:
#        if 'trip_update' in entity:
#            for update in entity.trip_update.stop_time_update:
#                if 'stop_id' in update and update.stop_id == stop_id:
#                    stop_time = {
#                        'trip_id': entity.trip_update.trip.trip_id,
#                        'arrival_time': update.arrival.time,
#                        'departure_time': update.departure.time,
#                        'delay': update.arrival.delay,
#                        'stop_sequence': update.stop_sequence,
#                    }
#                    stop_times.append(stop_time)

#    context = {'stop_details': stop_times}
#    return render(request, 'stop_details.html', context)
