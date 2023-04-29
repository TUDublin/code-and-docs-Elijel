from django.test import TestCase, Client
from django.urls import reverse
from .models import Stop

class AllStopsViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_all_stops_view_with_stop_id(self):
        stop = Stop.objects.create(
            stop_name='Parnell Square West, stop 2', 
            stop_id='8220DB000002',
            stop_lat=53.352244,
            stop_lon=-6.263723
        )
        url = reverse('main:allStops', args=[stop.stop_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, stop.stop_name)
        self.assertEqual(len(response.context['stop_lists']), 1)

    def test_all_stops_view_with_search_query(self):
        stop = Stop.objects.create(
            stop_name='Parnell Square West, stop 2', 
            stop_id='8220DB000002',
            stop_lat=53.352244,
            stop_lon=-6.263723
        )
        url = reverse('main:allStops')
        response = self.client.get(url, {'q': 'Parnell'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, stop.stop_name)

    def test_all_stops_view_without_stop_id_or_search_query(self):
        stop = Stop.objects.create(
            stop_name='Parnell Square West, stop 2', 
            stop_id='8220DB000002',
            stop_lat=53.352244,
            stop_lon=-6.263723
        )
        url = reverse('main:allStops')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, stop.stop_name)
