from django.core.management.base import BaseCommand
from django.contrib.postgres.search import SearchVector
from apps.jobs.models import Job

class Command(BaseCommand):
    help = 'Updates search vectors for all jobs'

    def handle(self, *args, **options):
        self.stdout.write('Updating search vectors...')
        
        Job.objects.update(search_vector=SearchVector(
            'title', 'description', 'location', 'requirements', 'company_name',
            config='english'
        ))
        
        self.stdout.write(self.style.SUCCESS('Successfully updated search vectors'))