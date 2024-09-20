from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Prints the current Django environment'

    def handle(self, *args, **kwargs):
        try:
            environment = settings.DJANGO_ENVIRONMENT
            self.stdout.write(self.style.SUCCESS(f'Current environment: {environment}'))
        except AttributeError:
            self.stdout.write(self.style.ERROR('DJANGO_ENVIRONMENT setting is not defined'))