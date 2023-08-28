from django.core.management.base import BaseCommand, CommandError

from stockouter.tasks import get_macrotrends_values


class Command(BaseCommand):
    help = "start parce macrotrends"

    def handle(self, *args, **options):
        return get_macrotrends_values()
