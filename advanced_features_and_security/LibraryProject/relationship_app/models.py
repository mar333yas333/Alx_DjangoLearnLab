"""
Relationship App Models with Permissions and Groups

This module defines the Book model with custom permissions for access control.
Permissions are enforced in views using @permission_required decorator.

Groups:
- Viewers: can_view only
- Editors: can_view, can_create, can_edit
- Admins: can_view, can_create, can_edit, can_delete

See PERMISSIONS_GROUPS_README.md for full documentation.
"""

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Book(models.Model):
    """
    Book model with custom permissions for granular access control.
    
    Custom Permissions:
    - can_view: User can view the list of books
    - can_create: User can create new book entries
    - can_edit: User can edit existing book entries
    - can_delete: User can delete book entries
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()

    def __str__(self):
        return self.title

    class Meta:
        """
        Custom permissions for Book model.
        Permissions are checked in views using @permission_required decorator.
        """
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# 🔔 Signal to auto-create UserProfile for every new user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='libraries')

    def __str__(self):
        return self.name


class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')

    def __str__(self):
        return self.name
    
    
