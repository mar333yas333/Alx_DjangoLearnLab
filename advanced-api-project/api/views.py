from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters
from django_filters import rest_framework  # type: ignore
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    Generic list view for retrieving all Book instances with filtering, searching, and ordering.
    
    HTTP Methods: GET
    Endpoint: GET /api/books/
    
    Behavior:
    - Retrieves and returns a list of all books in JSON format.
    - Allows read-only access to all users (authenticated and unauthenticated).
    - Supports filtering by title, author, and publication_year.
    - Supports text search on title and author fields.
    - Supports ordering by title and publication_year.
    
    Permissions:
    - IsAuthenticatedOrReadOnly: Unauthenticated users can view the list (GET),
      but cannot modify data.
    
    Serializer: BookSerializer
    Queryset: All Book objects.
    
    Filter Backends:
    - DjangoFilterBackend: Filter by title, author, publication_year
    - SearchFilter: Search in title and author fields
    - OrderingFilter: Sort by title and publication_year (default: ID)
    
    Query Parameters for Filtering:
    - ?title=The+Hobbit → Filter books by exact title
    - ?author=1 → Filter books by author ID
    - ?publication_year=1937 → Filter books by exact publication year
    
    Query Parameters for Searching:
    - ?search=Tolkien → Search for 'Tolkien' in title or author name
    - ?search=1937 → Search for '1937' in title or author name
    
    Query Parameters for Ordering:
    - ?ordering=title → Order results by title (ascending)
    - ?ordering=-title → Order results by title (descending)
    - ?ordering=publication_year → Order results by publication year (ascending)
    - ?ordering=-publication_year → Order results by publication year (descending)
    
    Examples:
    - GET /api/books/?title=The+Hobbit
    - GET /api/books/?author=1&publication_year=1937
    - GET /api/books/?search=Tolkien
    - GET /api/books/?ordering=-publication_year
    - GET /api/books/?search=Hobbit&ordering=title
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Configure filtering backends
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Fields to filter on using DjangoFilterBackend
    filterset_fields = ['title', 'author', 'publication_year']
    
    # Fields to search on using SearchFilter
    search_fields = ['title', 'author__name']
    
    # Fields to order on using OrderingFilter
    ordering_fields = ['title', 'publication_year']
    ordering = ['id']  # Default ordering


class BookDetailView(generics.RetrieveAPIView):
    """
    Generic detail view for retrieving a single Book instance by ID.
    
    HTTP Methods: GET
    Endpoint: GET /api/books/<int:pk>/
    
    Behavior:
    - Retrieves and returns a single book by its primary key (ID).
    - Includes related Author information via the serializer.
    - Allows read-only access to all users.
    
    Permissions:
    - IsAuthenticatedOrReadOnly: Unauthenticated users can retrieve a book (GET),
      but cannot modify data.
    
    Serializer: BookSerializer
    Queryset: All Book objects.
    Lookup Field: pk (primary key, default)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    Generic create view for adding a new Book instance.
    
    HTTP Methods: POST
    Endpoint: POST /api/books/create/
    
    Behavior:
    - Accepts POST requests with book data (title, publication_year, author).
    - Validates data using BookSerializer (including custom publication_year validation).
    - Creates and saves a new Book instance in the database.
    - Returns the created book data with its ID.
    
    Permissions:
    - IsAuthenticated: Only authenticated users can create books.
      Unauthenticated users receive a 403 Forbidden response.
    
    Serializer: BookSerializer
    Queryset: All Book objects (used for generating default response).
    
    Custom Behavior:
    - Data validation is handled by BookSerializer.validate_publication_year(),
      which ensures the publication year is not in the future.
    - If validation fails, the view returns a 400 Bad Request with error details.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    Generic update view for modifying an existing Book instance.
    
    HTTP Methods: PUT, PATCH
    Endpoint: PUT /api/books/<int:pk>/update/ or PATCH /api/books/<int:pk>/update/
    
    Behavior:
    - Accepts PUT (full update) or PATCH (partial update) requests.
    - PUT requires all fields; PATCH allows partial updates.
    - Validates data using BookSerializer.
    - Updates the book with the provided data.
    - Returns the updated book data.
    
    Permissions:
    - IsAuthenticated: Only authenticated users can update books.
      Unauthenticated users receive a 403 Forbidden response.
    
    Serializer: BookSerializer
    Queryset: All Book objects.
    Lookup Field: pk (primary key, default)
    
    Custom Behavior:
    - Custom validation in BookSerializer ensures publication_year is not in the future.
    - Partial updates (PATCH) allow updating only specific fields (e.g., title only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    Generic delete view for removing a Book instance.
    
    HTTP Methods: DELETE
    Endpoint: DELETE /api/books/<int:pk>/delete/
    
    Behavior:
    - Accepts DELETE requests to remove a specific book by ID.
    - Performs a hard delete (book is permanently removed from the database).
    - Returns a 204 No Content response on successful deletion.
    
    Permissions:
    - IsAuthenticated: Only authenticated users can delete books.
      Unauthenticated users receive a 403 Forbidden response.
    
    Serializer: BookSerializer
    Queryset: All Book objects.
    Lookup Field: pk (primary key, default)
    
    Custom Behavior:
    - Uses the default destroy() method which performs a hard delete.
    - No soft-delete or recovery mechanism is implemented.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
