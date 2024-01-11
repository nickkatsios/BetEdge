from __future__ import absolute_import, unicode_literals
from .arb_utils import *
import os
from .celery import app

# Define django settings at the top to be used accross all functions
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

# This is the function that will be called by the celery beat scheduler
@app.task(name="find_and_store_arbitrage_opportunities")
def find_and_store_arbitrage_opportunities():
    # arb utils call
    find_and_store_arbitrage_opportunities_football()

@app.task(name="purge_arbitrage_opportunities")
def purge_arbitrage_opportunities():
    """ Purge all arbitrage opportunities from the database."""
    Arbitrage.objects.all().delete()
    ArbitrageOutcomes.objects.all().delete()
    print("Purged all arbitrage opportunities from the database.")
