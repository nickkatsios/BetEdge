from rest_framework import serializers
from .models import *
"""
Serializers allow complex data such as querysets and model instances
to be converted to native Python datatypes that can then be easily
rendered into JSON, XML or other content types.
Serializers also provide deserialization, allowing parsed data
to be converted back into complex types, after first validating the incoming data.
"""

class OddsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Odds
        fields = "__all__"

class BookmakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmakers
        fields = "__all__"

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = "__all__"

class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Markets
        fields = "__all__"

class ArbitrageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arbitrage
        fields = "__all__"
