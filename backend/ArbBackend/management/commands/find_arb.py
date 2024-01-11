from django.core.management.base import BaseCommand
from ArbBackend.tasks import *

class Command(BaseCommand):
    help = 'Find and store arbitrage opportunities'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Finding and storing arbitrage opportunities...'))
        find_and_store_arbitrage_opportunities()
        self.stdout.write(self.style.SUCCESS('Arbitrage opportunities stored successfully.'))