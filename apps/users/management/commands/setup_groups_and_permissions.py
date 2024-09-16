# File: users/management/commands/setup_groups_and_permissions.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.jobs.models import Job
from apps.applications.models import Application
from apps.users.models import User

class Command(BaseCommand):
    help = 'Set up initial groups and permissions for the job board application'

    def handle(self, *args, **options):
        self.stdout.write('Setting up groups and permissions...')

        # Create groups
        job_seeker_group, created = Group.objects.get_or_create(name='JOB_SEEKER')
        self.stdout.write(f'{"Created" if created else "Retrieved"} JOB_SEEKER group')

        employer_group, created = Group.objects.get_or_create(name='EMPLOYER')
        self.stdout.write(f'{"Created" if created else "Retrieved"} EMPLOYER group')

        admin_group, created = Group.objects.get_or_create(name='ADMIN')
        self.stdout.write(f'{"Created" if created else "Retrieved"} ADMIN group')

        job_permissions = self._setup_model_permissions(Job)
        application_permissions = self._setup_model_permissions(Application)
        user_permissions = self._setup_model_permissions(User)

        self._assign_job_seeker_permissions(job_seeker_group, job_permissions, application_permissions)
        self._assign_employer_permissions(employer_group, job_permissions, application_permissions)
        self._assign_admin_permissions(admin_group, job_permissions, application_permissions, user_permissions)

        self.stdout.write(self.style.SUCCESS('Successfully set up groups and permissions'))

    def _setup_model_permissions(self, model):
        content_type = ContentType.objects.get_for_model(model)
        permissions = Permission.objects.filter(content_type=content_type)
        self.stdout.write(f'Set up permissions for {model.__name__}')
        return permissions

    def _assign_job_seeker_permissions(self, group, job_permissions, application_permissions):
        group.permissions.add(
            job_permissions.get(codename='view_job'),
            application_permissions.get(codename='add_application'),
            application_permissions.get(codename='view_application')
        )
        self.stdout.write(f'Assigned permissions to JOB_SEEKER group')

    def _assign_employer_permissions(self, group, job_permissions, application_permissions):
        group.permissions.add(
            *job_permissions,
            application_permissions.get(codename='view_application')
        )
        self.stdout.write(f'Assigned permissions to EMPLOYER group')

    def _assign_admin_permissions(self, group, job_permissions, application_permissions, user_permissions):
        group.permissions.add(
            *job_permissions,
            *application_permissions,
            *user_permissions
        )
        self.stdout.write(f'Assigned permissions to ADMIN group')