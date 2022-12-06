from .models import Realtime
from rest_framework import serializers

class CryptocurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Realtime
        fields = ['rt_trip_id', 'rt_route_id', 'rt_schedule', 'rt_stop_sequence', 'rt_stop_id']