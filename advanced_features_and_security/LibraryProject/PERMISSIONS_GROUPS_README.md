# Permissions and Groups Management Documentation

## Overview
This document explains how permissions and groups are configured and used in the Library Project to control access to Book operations.

## Custom Permissions

The `Book` model in `relationship_app/models.py` includes four custom permissions:

### Permission Definitions

| Permission Codename | Description | Used In |
|---|---|---|
| `can_view` | Can view books | `book_list` view |
| `can_create` | Can create new books | `add_book` view |
| `can_edit` | Can edit existing books | `edit_book` view |
| `can_delete` | Can delete books | `delete_book` view |

**Model Reference:**
```python
class Book(models.Model):
    # ... fields ...
    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]
```

## User Groups

Three predefined groups organize users by their access level:

### 1. **Viewers Group**
- **Permissions:** `can_view`
- **Use Case:** Users who can only view the list of books
- **Actions Allowed:**
  - View book list
  - View library details
  - Cannot create, edit, or delete books

### 2. **Editors Group**
- **Permissions:** `can_view`, `can_create`, `can_edit`
- **Use Case:** Librarians or content managers who can manage book information
- **Actions Allowed:**
  - View book list
  - Add new books
  - Edit existing books
  - Cannot delete books

### 3. **Admins Group**
- **Permissions:** `can_view`, `can_create`, `can_edit`, `can_delete`
- **Use Case:** Administrators with full control over books
- **Actions Allowed:**
  - All operations: view, create, edit, delete books

## Setting Up Groups and Permissions

### Automatic Setup (Recommended)

Run the included management command to automatically create groups and assign permissions:

```bash
python manage.py setup_groups
```

This command:
1. Creates the three groups (Viewers, Editors, Admins)
2. Fetches custom permissions from the Book model
3. Assigns appropriate permissions to each group

### Manual Setup via Django Admin

1. Log in to Django admin (`/admin/`)
2. Navigate to **Authentication and Authorization** → **Groups**
3. Create three groups:
   - **Viewers**: Assign `can_view`
   - **Editors**: Assign `can_view`, `can_create`, `can_edit`
   - **Admins**: Assign `can_view`, `can_create`, `can_edit`, `can_delete`

### Programmatic Setup

```python
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book

# Get permissions
content_type = ContentType.objects.get_for_model(Book)
can_view = Permission.objects.get(content_type=content_type, codename='can_view')
can_create = Permission.objects.get(content_type=content_type, codename='can_create')
can_edit = Permission.objects.get(content_type=content_type, codename='can_edit')
can_delete = Permission.objects.get(content_type=content_type, codename='can_delete')

# Create groups and assign permissions
viewers, _ = Group.objects.get_or_create(name='Viewers')
viewers.permissions.set([can_view])

editors, _ = Group.objects.get_or_create(name='Editors')
editors.permissions.set([can_view, can_create, can_edit])

admins, _ = Group.objects.get_or_create(name='Admins')
admins.permissions.set([can_view, can_create, can_edit, can_delete])
```

## Assigning Users to Groups

### Via Django Admin

1. Go to **Authentication and Authorization** → **Users**
2. Select a user
3. Scroll to **Groups** section
4. Check the groups to assign (e.g., Editors)
5. Save

### Programmatically

```python
from django.contrib.auth.models import Group
from users.models import CustomUser

user = CustomUser.objects.get(email='user@example.com')
editors_group = Group.objects.get(name='Editors')
user.groups.add(editors_group)

# Or remove from a group:
user.groups.remove(editors_group)
```

## Views and Permission Enforcement

All relevant views in `relationship_app/views.py` use the `@permission_required` decorator with `raise_exception=True` to enforce permissions:

### Views Protected

| View | Required Permission | HTTP Status on Denied |
|---|---|---|
| `book_list` | `relationship_app.can_view` | 403 Forbidden |
| `add_book` | `relationship_app.can_create` | 403 Forbidden |
| `edit_book` | `relationship_app.can_edit` | 403 Forbidden |
| `delete_book` | `relationship_app.can_delete` | 403 Forbidden |

### Example: add_book View

```python
@permission_required('relationship_app.can_create', raise_exception=True)
def add_book(request):
    """
    View to add a new book.
    Requires can_create permission.
    Raises 403 Forbidden if user lacks permission.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        published_date = request.POST.get('published_date')
        Book.objects.create(
            title=title,
            author=author,
            published_date=published_date
        )
        return redirect('list_books')
    return render(request, 'relationship_app/add_book.html')
```

## Testing Permissions

### Manual Testing Steps

1. **Create test users:**
   ```bash
   python manage.py shell
   ```
   ```python
   from users.models import CustomUser
   viewer = CustomUser.objects.create_user(email='viewer@test.com', username='viewer', password='test123')
   editor = CustomUser.objects.create_user(email='editor@test.com', username='editor', password='test123')
   admin = CustomUser.objects.create_user(email='admin@test.com', username='admin', password='test123')
   ```

2. **Assign users to groups:**
   ```python
   from django.contrib.auth.models import Group
   viewers_group = Group.objects.get(name='Viewers')
   editors_group = Group.objects.get(name='Editors')
   admins_group = Group.objects.get(name='Admins')
   
   viewer.groups.add(viewers_group)
   editor.groups.add(editors_group)
   admin.groups.add(admins_group)
   ```

3. **Test access:**
   - Log in as **viewer**: Can view books, cannot create/edit/delete
   - Log in as **editor**: Can view, create, edit; cannot delete
   - Log in as **admin**: Can view, create, edit, delete all

4. **Verify 403 responses:**
   - Viewer visits `/books/add/` → 403 Forbidden
   - Editor visits `/books/1/delete/` → 403 Forbidden
   - Admin can access all URLs

### Automated Testing (Optional)

Create unit tests in `relationship_app/tests.py` to verify permissions are enforced:

```python
from django.test import TestCase, Client
from django.contrib.auth.models import Group
from users.models import CustomUser
from relationship_app.models import Book

class PermissionTestCase(TestCase):
    def setUp(self):
        # Create user and assign to Viewers group
        self.client = Client()
        self.viewer = CustomUser.objects.create_user(
            email='viewer@test.com',
            username='viewer',
            password='test123'
        )
        viewers_group = Group.objects.get(name='Viewers')
        self.viewer.groups.add(viewers_group)
        
    def test_viewer_cannot_add_book(self):
        self.client.login(email='viewer@test.com', password='test123')
        response = self.client.get('/books/add/')
        self.assertEqual(response.status_code, 403)
        
    def test_viewer_can_view_books(self):
        self.client.login(email='viewer@test.com', password='test123')
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)
```

## Configuration Summary

| Aspect | Configuration |
|---|---|
| **Permissions Location** | `relationship_app/models.py` - Book model Meta class |
| **Group Setup** | `relationship_app/management/commands/setup_groups.py` |
| **Permission Enforcement** | `relationship_app/views.py` - All book operation views |
| **Authentication** | `users.models.CustomUser` |
| **Admin Management** | Django admin panel at `/admin/` |

## Security Notes

1. **Always use `raise_exception=True`** in `@permission_required` to return 403 instead of redirecting to login
2. **Regularly audit user groups** to ensure least-privilege access
3. **Test permissions** before deploying to production
4. **Document role changes** for compliance and auditing
5. **Never hardcode permissions** — always use the permission system

## Troubleshooting

**Issue:** Permissions not found after running `setup_groups`
- **Solution:** Run `python manage.py migrate` first to create permissions

**Issue:** User can still access protected views
- **Solution:** Verify user is added to a group with appropriate permissions via Django admin

**Issue:** New permissions not appearing in Django admin
- **Solution:** Run migrations and restart Django development server

---

**Last Updated:** November 14, 2025
