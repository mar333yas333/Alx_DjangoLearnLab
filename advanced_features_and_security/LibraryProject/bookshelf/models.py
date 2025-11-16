from django.db import models

class Book(models.Model):
    """
    Book model with custom permissions for granular access control.
    
    Custom Permissions:
    - can_view: User can view the list of books
    - can_create: User can create new book entries
    - can_edit: User can edit existing book entries
    - can_delete: User can delete book entries
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField(null=True, blank=True)

    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]

    def __str__(self):
        return self.title
