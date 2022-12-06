from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from main.models import Stop
from django.db.models import Q

def searchResult(request):
    stops = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        stops = Stop.objects.all().filter(Q(stop_name__contains=query))
    else:
        stops = Stop.objects.all().filter()

    '''Pagination Code'''
    paginator = Paginator(stops, 100)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        stop_lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        stop_lists = paginator.page(paginator.num_pages)
    return render(request,'search.html',{'query':query, 'stop_lists':stop_lists})