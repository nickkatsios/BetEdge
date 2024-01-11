from django.core.management.base import BaseCommand
from ArbBackend.tasks import *

class Command(BaseCommand):
    help = 'Delete all arbitrage opportunities and their outcomes from the database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Deleting arbitrage opportunities...'))
        purge_arbitrage_opportunities()
        self.stdout.write(self.style.SUCCESS('Arbitrage opportunities deleted successfully.'))