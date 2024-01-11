from django.contrib import admin
from .models import Bookmakers, Events, Markets, Odds, Arbitrage, Urls, ArbitrageOutcomes

# Register your models here to be shown in the admin panel.
admin.site.register(Bookmakers)
admin.site.register(Events)
admin.site.register(Markets)
admin.site.register(Odds)
admin.site.register(Arbitrage)
admin.site.register(ArbitrageOutcomes)
admin.site.register(Urls)
