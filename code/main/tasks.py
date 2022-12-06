from time import sleep
from celery import shared_task
from django.shortcuts import render
import requests

from .models import Realtime

def Convert(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct

@shared_task
def crawl_currency():
    url='https://api.nationaltransport.ie/gtfsr/v1?format=json'

    headers = {
        'X-API-KEY': 'ddece4bcc95b497f97aaa72b96617dca',
        'Content-Type': 'application/json; charset=utf-8',
        'User-agent': 'your bot 0.1'
    }

    response = requests.get(url, headers=headers, verify=True).json()

    for each in range(len(response["Entity"])):
        for items in range(len(response["Entity"][each]["TripUpdate"]["StopTimeUpdate"])):
            if "Arrival" in range(len(response["Entity"][each]["TripUpdate"]["StopTimeUpdate"] is not None)):
                    rt_trip_id = (response["Entity"][each]["TripUpdate"]["Trip"]["TripId"]) #TripID
                    rt_route_id = (response["Entity"][each]["TripUpdate"]["Trip"]["RouteId"]) #RouteId
                    rt_schedule = (response["Entity"][each]["TripUpdate"]["Trip"]["ScheduleRelationship"]) #ScheduleRelationship
                    rt_stop_sequence = (response["Entity"][each]["TripUpdate"]["StopTimeUpdate"][items]["StopSequence"]) #StopSequence
                    rt_stop_id = (response["Entity"][each]["TripUpdate"]["StopTimeUpdate"][items]["StopId"]) #StopId
                    rt_delay = (response["Entity"][each]["TripUpdate"]["StopTimeUpdate"][items]["StopId"]["Arrival"["Delay"]]) #StopId
                    print({'rt_trip_id': rt_trip_id, 'rt_route_id':rt_route_id, 'rt_schedule':rt_schedule, 'rt_stop_sequence':rt_stop_sequence, 'rt_stop_id':rt_stop_id}) 
            else:
                rt_trip_id = (response["Entity"][each]["TripUpdate"]["Trip"]["TripId"]) #TripID
                rt_route_id = (response["Entity"][each]["TripUpdate"]["Trip"]["RouteId"]) #RouteId
                rt_schedule = (response["Entity"][each]["TripUpdate"]["Trip"]["ScheduleRelationship"]) #ScheduleRelationship
                rt_stop_sequence = (response["Entity"][each]["TripUpdate"]["StopTimeUpdate"][items]["StopSequence"]) #StopSequence
                rt_stop_id = (response["Entity"][each]["TripUpdate"]["StopTimeUpdate"][items]["StopId"]) #StopId
                print({'rt_trip_id': rt_trip_id, 'rt_route_id':rt_route_id, 'rt_schedule':rt_schedule, 'rt_stop_sequence':rt_stop_sequence, 'rt_stop_id':rt_stop_id}) 
        Realtime.objects.create(
            rt_trip_id = rt_trip_id,
            rt_route_id = rt_route_id,
            rt_schedule = rt_schedule,
            rt_stop_sequence = rt_stop_sequence,
            rt_stop_id = rt_stop_id
        )

@shared_task
def update_currency():
    url='https://api.nationaltransport.ie/gtfsr/v1?format=json'

    headers = {
        'X-API-KEY': 'ddece4bcc95b497f97aaa72b96617dca',
        'Content-Type': 'application/json; charset=utf-8',
        'User-agent': 'your bot 0.1'
    }

    response = requests.get(url, headers=headers, verify=True).json()

    for each in range(len(response["Entity"])):
        for items in range(len(response["Entity"][each]["TripUpdate"]["StopTimeUpdate"])):
            if "Arrival" in range(len(response["Entity"][each]["TripUpdate"]["StopTimeUpdate"] is not None)):
                    rt_trip_id = (response["Entity"][each]["TripUpdate"]["Trip"]["TripId"]) #TripID
                    rt_route_id = (response["Entity"][each]["TripUpdate"]["Trip"]["RouteId"]) #RouteId
                    rt_schedule = (response["Entity"][each]["TripUpdate"]["Trip"]["ScheduleRelationship"]) #ScheduleRelationship
                    rt_stop_sequence = (response["Entity"][each]["TripUpdate"]["StopTimeUpdate"][items]["StopSequence"]) #StopSequence
                    rt_stop_id = (response["Entity"][each]["TripUpdate"]["StopTimeUpdate"][items]["StopId"]) #StopId
                    rt_delay = (response["Entity"][each]["TripUpdate"]["StopTimeUpdate"][items]["StopId"]["Arrival"["Delay"]]) #StopId
                    data = print({'rt_trip_id': rt_trip_id, 'rt_route_id':rt_route_id, 'rt_schedule':rt_schedule, 'rt_stop_sequence':rt_stop_sequence, 'rt_stop_id':rt_stop_id}) 
            else:
                rt_trip_id = (response["Entity"][each]["TripUpdate"]["Trip"]["TripId"]) #TripID
                rt_route_id = (response["Entity"][each]["TripUpdate"]["Trip"]["RouteId"]) #RouteId
                rt_schedule = (response["Entity"][each]["TripUpdate"]["Trip"]["ScheduleRelationship"]) #ScheduleRelationship
                rt_stop_sequence = (response["Entity"][each]["TripUpdate"]["StopTimeUpdate"][items]["StopSequence"]) #StopSequence
                rt_stop_id = (response["Entity"][each]["TripUpdate"]["StopTimeUpdate"][items]["StopId"]) #StopId
                data = print({'rt_trip_id': rt_trip_id, 'rt_route_id':rt_route_id, 'rt_schedule':rt_schedule, 'rt_stop_sequence':rt_stop_sequence, 'rt_stop_id':rt_stop_id}) 
        Realtime.objects.filter(rt_trip_id=rt_trip_id).update(**(data, 'none'))

#if not Realtime.objects:      
    #crawl_currency()

#while True:
    #sleep(5)
    #update_currency()