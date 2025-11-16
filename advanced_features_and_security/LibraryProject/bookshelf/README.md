# Bookshelf Permissions System

This app demonstrates how to use Django permissions and groups.

## Custom Permissions
Defined in Book model:
- can_view
- can_create
- can_edit
- can_delete

## Groups
Configured via Django admin:
- Viewers: can_view
- Editors: can_view, can_create, can_edit
- Admins: all permissions

## Views
Each action is protected using @permission_required with raise_exception=True.
