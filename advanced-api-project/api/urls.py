from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

"""
URL Configuration for the api app.

This module defines all API endpoints for Book CRUD operations.
Each endpoint is mapped to its corresponding generic view with appropriate HTTP methods.

Endpoints Summary:
- GET /api/books/                    → BookListView (retrieve all books)
- GET /api/books/<int:pk>/           → BookDetailView (retrieve a single book by ID)
- POST /api/books/create/            → BookCreateView (create a new book)
- PUT /api/books/<int:pk>/update/    → BookUpdateView (full update of a book)
- PATCH /api/books/<int:pk>/update/  → BookUpdateView (partial update of a book)
- DELETE /api/books/<int:pk>/delete/ → BookDeleteView (delete a book)

Permission Notes:
- List and Detail views: IsAuthenticatedOrReadOnly (read access for all, write for authenticated)
- Create view: IsAuthenticated (only authenticated users can create)
- Update view: IsAuthenticated (only authenticated users can update)
- Delete view: IsAuthenticated (only authenticated users can delete)

Testing Notes:
- Use /api/token-auth/ (from main urls.py) to obtain an authentication token.
- Include token in Authorization header: Authorization: Token <your-token>
"""

urlpatterns = [
    # List all books (read-only for unauthenticated users)
    path('books/', BookListView.as_view(), name='book-list'),
    
    # Retrieve a single book by ID (read-only for unauthenticated users)
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # Create a new book (authenticated users only)
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    
    # Update an existing book (authenticated users only)
    # Supports both PUT (full update) and PATCH (partial update)
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),
    
    # Delete an existing book (authenticated users only)
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),
]
