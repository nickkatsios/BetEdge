from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework import generics

class BookmakersList(generics.ListAPIView):
    """ Retrieve all bookmakers or create a new one."""
    queryset = Bookmakers.objects.all()
    serializer_class = BookmakerSerializer

class BookmakerDetails(generics.RetrieveAPIView):
    """ Retrieve a single bookmaker by its ID."""
    queryset = Bookmakers.objects.all()
    serializer_class = BookmakerSerializer

class EventsList(generics.ListAPIView):
    """ Retrieve all events or create a new one."""
    queryset = Events.objects.all()
    serializer_class = EventSerializer

class EventDetails(generics.RetrieveAPIView):
    """ Retrieve a single event by its ID."""
    queryset = Events.objects.all()
    serializer_class = EventSerializer

class MarketsList(generics.ListAPIView):
    """ Retrieve all markets or create a new one."""
    queryset = Markets.objects.all()
    serializer_class = MarketSerializer

class MarketDetails(generics.RetrieveAPIView):
    """ Retrieve a single market by its ID."""
    queryset = Markets.objects.all()
    serializer_class = MarketSerializer

class ArbitrageList(generics.ListAPIView):
    """ Retrieve all arbitrage opportunities."""
    queryset = Arbitrage.objects.all()
    serializer_class = ArbitrageSerializer



