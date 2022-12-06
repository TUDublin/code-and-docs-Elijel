from .models import Stop

def menu_links(request):
    links= Stop.objects.all()
    return dict(links=links)