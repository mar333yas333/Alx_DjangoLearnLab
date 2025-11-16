"""
Management command to set up groups and assign permissions.

This command creates three groups:
- Viewers: Can view books (can_view)
- Editors: Can view, create, and edit books (can_view, can_create, can_edit)
- Admins: Can perform all operations (can_view, can_create, can_edit, can_delete)

Usage:
    python manage.py setup_groups
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book


class Command(BaseCommand):
    help = 'Set up groups and assign permissions for Book model'

    def handle(self, *args, **options):
        # Get permissions for Book model
        content_type = ContentType.objects.get_for_model(Book)
        
        try:
            can_view = Permission.objects.get(
                content_type=content_type,
                codename='can_view'
            )
            can_create = Permission.objects.get(
                content_type=content_type,
                codename='can_create'
            )
            can_edit = Permission.objects.get(
                content_type=content_type,
                codename='can_edit'
            )
            can_delete = Permission.objects.get(
                content_type=content_type,
                codename='can_delete'
            )
        except Permission.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    'Permissions not found. Make sure to run migrations first.'
                )
            )
            return

        # Create or get groups
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        editors_group, created = Group.objects.get_or_create(name='Editors')
        admins_group, created = Group.objects.get_or_create(name='Admins')

        # Assign permissions to Viewers group
        viewers_group.permissions.set([can_view])
        self.stdout.write(
            self.style.SUCCESS(
                'Assigned can_view permission to Viewers group'
            )
        )

        # Assign permissions to Editors group
        editors_group.permissions.set([can_view, can_create, can_edit])
        self.stdout.write(
            self.style.SUCCESS(
                'Assigned can_view, can_create, can_edit permissions to Editors group'
            )
        )

        # Assign permissions to Admins group
        admins_group.permissions.set(
            [can_view, can_create, can_edit, can_delete]
        )
        self.stdout.write(
            self.style.SUCCESS(
                'Assigned all permissions to Admins group'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                '\nGroups and permissions setup completed successfully!'
            )
        )
        self.stdout.write(
            self.style.WARNING(
                '\nReminder: Assign users to groups via Django admin or programmatically.'
            )
        )
