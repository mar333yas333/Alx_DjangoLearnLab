# Advanced API Project - Custom Generic Views with Django REST Framework

## Overview

This project demonstrates how to build a REST API using Django REST Framework with custom generic views, proper permission handling, and comprehensive documentation. The API provides CRUD operations for managing books and their authors with role-based access control.

## Project Structure

```
advanced-api-project/
├── manage.py
├── db.sqlite3
├── advanced_api_project/          # Main project package
│   ├── __init__.py
│   ├── settings.py                # Django settings (DRF configured)
│   ├── urls.py                    # Main URL router
│   ├── wsgi.py
│   └── asgi.py
├── api/                           # Django app with models and views
│   ├── __init__.py
│   ├── models.py                  # Author and Book models
│   ├── serializers.py             # BookSerializer and AuthorSerializer
│   ├── views.py                   # Generic CRUD views
│   ├── urls.py                    # API URL patterns
│   ├── admin.py                   # Django admin configuration
│   ├── apps.py
│   ├── tests.py
│   └── migrations/
└── README.md                      # This file
```

## Models

### Author
- **name** (CharField): The author's name
- Relationship: One-to-many with Book (via related_name='books')

### Book
- **title** (CharField): The book's title
- **publication_year** (IntegerField): Year the book was published
- **author** (ForeignKey): Reference to the Author model

## API Endpoints

All endpoints are prefixed with `/api/`.

### 1. List All Books
**Endpoint:** `GET /api/books/`
- **Permission:** IsAuthenticatedOrReadOnly (read for all, write for authenticated)
- **Response:** JSON array of all books
- **Example:**
  ```bash
  curl http://127.0.0.1:8000/api/books/
  ```

### 2. Retrieve a Single Book
**Endpoint:** `GET /api/books/<int:pk>/`
- **Permission:** IsAuthenticatedOrReadOnly
- **Response:** JSON object for the book with ID `pk`
- **Example:**
  ```bash
  curl http://127.0.0.1:8000/api/books/1/
  ```

### 3. Create a New Book
**Endpoint:** `POST /api/books/create/`
- **Permission:** IsAuthenticated (authenticated users only)
- **Request Body:**
  ```json
  {
    "title": "The Hobbit",
    "publication_year": 1937,
    "author": 1
  }
  ```
- **Response:** JSON object of the created book with ID
- **Validation:** 
  - publication_year must not be in the future
- **Example:**
  ```bash
  curl -X POST -H "Authorization: Token <your-token>" \
       -H "Content-Type: application/json" \
       -d '{"title":"Dune","publication_year":1965,"author":1}' \
       http://127.0.0.1:8000/api/books/create/
  ```

### 4. Update an Existing Book
**Endpoint:** `PUT /api/books/<int:pk>/update/` or `PATCH /api/books/<int:pk>/update/`
- **Permission:** IsAuthenticated
- **Methods:**
  - **PUT:** Full update (all fields required)
  - **PATCH:** Partial update (only changed fields required)
- **Request Body (example for PATCH):**
  ```json
  {
    "title": "The Hobbit - Revised Edition"
  }
  ```
- **Response:** JSON object of the updated book
- **Validation:** publication_year must not be in the future
- **Examples:**
  ```bash
  # Full update (PUT)
  curl -X PUT -H "Authorization: Token <your-token>" \
       -H "Content-Type: application/json" \
       -d '{"title":"Updated Title","publication_year":1950,"author":1}' \
       http://127.0.0.1:8000/api/books/1/update/

  # Partial update (PATCH)
  curl -X PATCH -H "Authorization: Token <your-token>" \
       -H "Content-Type: application/json" \
       -d '{"title":"New Title"}' \
       http://127.0.0.1:8000/api/books/1/update/
  ```

### 5. Delete a Book
**Endpoint:** `DELETE /api/books/<int:pk>/delete/`
- **Permission:** IsAuthenticated
- **Response:** 204 No Content (on success)
- **Example:**
  ```bash
  curl -X DELETE -H "Authorization: Token <your-token>" \
       http://127.0.0.1:8000/api/books/1/delete/
  ```

## Filtering, Searching, and Ordering

The `/api/books/` endpoint supports advanced query capabilities for enhanced data retrieval.

### Filtering

Filter books by specific fields using query parameters:

**Available filter fields:**
- `title` — Filter by book title
- `author` — Filter by author ID
- `publication_year` — Filter by publication year

**Examples:**
```bash
# Filter by title
curl http://127.0.0.1:8000/api/books/?title=The+Hobbit

# Filter by author ID
curl http://127.0.0.1:8000/api/books/?author=1

# Filter by publication year
curl http://127.0.0.1:8000/api/books/?publication_year=1937

# Combine multiple filters
curl http://127.0.0.1:8000/api/books/?author=1&publication_year=1937
```

### Searching

Perform full-text search across title and author name fields:

**Searchable fields:**
- `title` — Book title
- `author__name` — Author's name

**Examples:**
```bash
# Search for 'Tolkien' in title or author name
curl http://127.0.0.1:8000/api/books/?search=Tolkien

# Search for a book title
curl http://127.0.0.1:8000/api/books/?search=Hobbit

# Search for a publication year as text
curl http://127.0.0.1:8000/api/books/?search=1937
```

### Ordering

Sort results by specific fields in ascending or descending order:

**Available ordering fields:**
- `title` — Sort by book title
- `publication_year` — Sort by publication year
- Prefix with `-` for descending order (e.g., `-publication_year`)

**Examples:**
```bash
# Sort by title (ascending)
curl http://127.0.0.1:8000/api/books/?ordering=title

# Sort by title (descending)
curl http://127.0.0.1:8000/api/books/?ordering=-title

# Sort by publication year (ascending)
curl http://127.0.0.1:8000/api/books/?ordering=publication_year

# Sort by publication year (descending, most recent first)
curl http://127.0.0.1:8000/api/books/?ordering=-publication_year
```

### Combined Query Examples

You can combine filtering, searching, and ordering:

```bash
# Search for 'Tolkien' and sort by title
curl http://127.0.0.1:8000/api/books/?search=Tolkien&ordering=title

# Filter by author ID and sort by publication year (descending)
curl http://127.0.0.1:8000/api/books/?author=1&ordering=-publication_year

# Search for a book and filter by publication year, sorted by title
curl http://127.0.0.1:8000/api/books/?search=Hobbit&publication_year=1937&ordering=title
```

## Authentication

### Token Authentication
This API uses token-based authentication for write operations.

**Obtaining a Token:**
1. First, create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

2. Use your credentials to obtain a token (endpoint in main urls.py):
   ```bash
   curl -X POST -d "username=your_username&password=your_password" \
        http://127.0.0.1:8000/api/token-auth/
   ```
   Response:
   ```json
   {"token":"abc123xyz..."}
   ```

3. Use the token in subsequent requests:
   ```bash
   curl -H "Authorization: Token abc123xyz..." http://127.0.0.1:8000/api/books/
   ```

## Permissions

| Endpoint | Method | Permission | Notes |
|----------|--------|-----------|-------|
| /books/ | GET | IsAuthenticatedOrReadOnly | Read for all, write for authenticated |
| /books/<id>/ | GET | IsAuthenticatedOrReadOnly | Read for all, write for authenticated |
| /books/create/ | POST | IsAuthenticated | Authenticated users only |
| /books/<id>/update/ | PUT/PATCH | IsAuthenticated | Authenticated users only |
| /books/<id>/delete/ | DELETE | IsAuthenticated | Authenticated users only |

## View Implementations

All views are generic views from Django REST Framework:

- **BookListView** (ListAPIView): Retrieve all books
- **BookDetailView** (RetrieveAPIView): Retrieve a single book
- **BookCreateView** (CreateAPIView): Create a new book
- **BookUpdateView** (UpdateAPIView): Update an existing book
- **BookDeleteView** (DestroyAPIView): Delete a book

Each view includes:
- Detailed docstrings explaining behavior
- Permission classes for access control
- Serializer integration for data validation
- Proper HTTP method handling

## Testing the API

### Setup
1. Install dependencies:
   ```bash
   pip install django djangorestframework
   ```

2. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Testing Without Authentication (Read-Only)
```bash
# List all books
curl http://127.0.0.1:8000/api/books/

# Get a single book
curl http://127.0.0.1:8000/api/books/1/
```

### Testing With Authentication (Full CRUD)
1. Obtain a token:
   ```bash
   curl -X POST -d "username=admin&password=your_password" \
        http://127.0.0.1:8000/api/token-auth/
   ```

2. Use the token for authenticated operations:
   ```bash
   # Create a book
   curl -X POST -H "Authorization: Token <your-token>" \
        -H "Content-Type: application/json" \
        -d '{"title":"New Book","publication_year":2023,"author":1}' \
        http://127.0.0.1:8000/api/books/create/

   # Update a book
   curl -X PATCH -H "Authorization: Token <your-token>" \
        -H "Content-Type: application/json" \
        -d '{"title":"Updated Title"}' \
        http://127.0.0.1:8000/api/books/1/update/

   # Delete a book
   curl -X DELETE -H "Authorization: Token <your-token>" \
        http://127.0.0.1:8000/api/books/1/delete/
   ```

### Using Postman
1. **Create a new request** with method GET
2. **URL:** http://127.0.0.1:8000/api/books/
3. For authenticated requests:
   - Go to **Headers** tab
   - Add header: `Authorization: Token <your-token>`
4. Send the request

## Custom Serializer Validation

The `BookSerializer` includes custom validation for `publication_year`:
- **Rule:** publication_year cannot be in the future
- **Error Response:** 400 Bad Request with validation error details
- **Example Error:**
  ```json
  {
    "publication_year": [
      "Publication year cannot be in the future. Current year is 2025."
    ]
  }
  ```

## Nested Serialization

The `AuthorSerializer` uses nested serialization to include all related books:
```json
{
  "id": 1,
  "name": "J.R.R. Tolkien",
  "books": [
    {
      "id": 1,
      "title": "The Hobbit",
      "publication_year": 1937,
      "author": 1
    },
    {
      "id": 2,
      "title": "The Lord of the Rings",
      "publication_year": 1954,
      "author": 1
    }
  ]
}
```

## Development Notes

### Adding More Views
To add additional views:
1. Create a new view class in `api/views.py` extending an appropriate generic view
2. Add the URL pattern to `api/urls.py`
3. Include any necessary permissions in the view class
4. Document the view with detailed docstrings

### Customizing Permissions
To use different permission classes:
- Replace `permission_classes = [permissions.IsAuthenticated]` in the view with your desired permission class
- Available options: `IsAuthenticated`, `IsAdminUser`, `IsAuthenticatedOrReadOnly`, or custom permission classes

### Extending Serializer Validation
To add more custom validation:
1. Add a `validate_<field_name>()` method in the serializer
2. Raise `serializers.ValidationError` if validation fails
3. Return the value if validation passes

## Resources

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [Generic Views](https://www.django-rest-framework.org/api-guide/generic-views/)
- [Permissions](https://www.django-rest-framework.org/api-guide/permissions/)
- [Serializers](https://www.django-rest-framework.org/api-guide/serializers/)
