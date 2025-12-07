"""
Unit Tests for Django REST Framework API Endpoints

This module contains comprehensive unit tests for the Book API endpoints,
covering CRUD operations, filtering, searching, ordering, and permission enforcement.

Testing Strategy:
- Use Django's TestCase class for database transaction rollback after each test
- Use Django REST Framework's APIClient for making API requests
- Test with and without authentication to verify permission enforcement
- Verify correct status codes and response data for all endpoints
- Test filtering, searching, and ordering query parameters

Test Coverage:
1. Book List View (GET /api/books/)
   - Retrieve all books without authentication (allowed)
   - Retrieve books with filtering by title, author, publication_year
   - Retrieve books with search parameters
   - Retrieve books with ordering parameters

2. Book Detail View (GET /api/books/<id>/)
   - Retrieve a single book without authentication (allowed)
   - Retrieve a non-existent book (404 error)

3. Book Create View (POST /api/books/create/)
   - Create a book with authentication (allowed)
   - Create a book without authentication (401 error)
   - Create a book with invalid publication_year (future year - 400 error)
   - Verify created book is in database

4. Book Update View (PUT/PATCH /api/books/update/<id>/)
   - Update a book with authentication (allowed)
   - Update a book without authentication (401 error)
   - Partial update with PATCH
   - Verify updated data is saved correctly

5. Book Delete View (DELETE /api/books/delete/<id>/)
   - Delete a book with authentication (allowed)
   - Delete a book without authentication (401 error)
   - Verify deleted book is removed from database

How to Run Tests:
- Run all tests: python manage.py test api
- Run specific test class: python manage.py test api.test_views.BookListViewTests
- Run specific test method: python manage.py test api.test_views.BookListViewTests.test_get_all_books
- Run with verbose output: python manage.py test api -v 2
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import Author, Book
from datetime import datetime


class BookListViewTests(APITestCase):
    """Test cases for Book List View (GET /api/books/)"""
    
    def setUp(self):
        """Set up test data and API client"""
        self.client = APIClient()
        
        # Create test author
        self.author = Author.objects.create(name="J.R.R. Tolkien")
        
        # Create test books
        self.book1 = Book.objects.create(
            title="The Hobbit",
            publication_year=1937,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title="The Lord of the Rings",
            publication_year=1954,
            author=self.author
        )
        
        # Create another author and book
        self.author2 = Author.objects.create(name="Isaac Asimov")
        self.book3 = Book.objects.create(
            title="Foundation",
            publication_year=1951,
            author=self.author2
        )
    
    def test_get_all_books_unauthenticated(self):
        """Test retrieving all books without authentication (should be allowed)"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_filter_by_title(self):
        """Test filtering books by title"""
        response = self.client.get('/api/books/?title=The+Hobbit')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Note: Exact match filtering
        self.assertTrue(any(book['title'] == 'The Hobbit' for book in response.data))
    
    def test_filter_by_author(self):
        """Test filtering books by author ID"""
        response = self.client.get(f'/api/books/?author={self.author.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return 2 books by Tolkien
        self.assertEqual(len(response.data), 2)
    
    def test_filter_by_publication_year(self):
        """Test filtering books by publication year"""
        response = self.client.get('/api/books/?publication_year=1937')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(book['publication_year'] == 1937 for book in response.data))
    
    def test_search_by_title(self):
        """Test searching books by title"""
        response = self.client.get('/api/books/?search=Hobbit')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any('Hobbit' in book['title'] for book in response.data))
    
    def test_search_by_author_name(self):
        """Test searching books by author name"""
        response = self.client.get('/api/books/?search=Tolkien')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should find books by Tolkien
        self.assertEqual(len(response.data), 2)
    
    def test_ordering_by_title_ascending(self):
        """Test ordering books by title in ascending order"""
        response = self.client.get('/api/books/?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))
    
    def test_ordering_by_title_descending(self):
        """Test ordering books by title in descending order"""
        response = self.client.get('/api/books/?ordering=-title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))
    
    def test_ordering_by_publication_year(self):
        """Test ordering books by publication year"""
        response = self.client.get('/api/books/?ordering=publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years))


class BookDetailViewTests(APITestCase):
    """Test cases for Book Detail View (GET /api/books/<id>/)"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.author = Author.objects.create(name="J.R.R. Tolkien")
        self.book = Book.objects.create(
            title="The Hobbit",
            publication_year=1937,
            author=self.author
        )
    
    def test_get_book_detail_unauthenticated(self):
        """Test retrieving a single book without authentication"""
        response = self.client.get(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'The Hobbit')
        self.assertEqual(response.data['publication_year'], 1937)
    
    def test_get_nonexistent_book(self):
        """Test retrieving a non-existent book returns 404"""
        response = self.client.get('/api/books/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookCreateViewTests(APITestCase):
    """Test cases for Book Create View (POST /api/books/create/)"""
    
    def setUp(self):
        """Set up test data and authentication"""
        self.client = APIClient()
        self.author = Author.objects.create(name="J.R.R. Tolkien")
        
        # Create a test user for authentication
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_create_book_unauthenticated(self):
        """Test creating a book without authentication (should be rejected)"""
        book_data = {
            'title': 'New Book',
            'publication_year': 2020,
            'author': self.author.id
        }
        response = self.client.post('/api/books/create/', book_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_book_authenticated(self):
        """Test creating a book with authentication (should be allowed)"""
        # Log in user via session authentication
        self.client.login(username='testuser', password='testpass123')
        
        book_data = {
            'title': 'New Book',
            'publication_year': 2020,
            'author': self.author.id
        }
        response = self.client.post('/api/books/create/', book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify book was created in database
        self.assertTrue(Book.objects.filter(title='New Book').exists())
    
    def test_create_book_with_future_publication_year(self):
        """Test creating a book with future publication year (should be rejected)"""
        self.client.login(username='testuser', password='testpass123')
        
        future_year = datetime.now().year + 1
        book_data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author.id
        }
        response = self.client.post('/api/books/create/', book_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)


class BookUpdateViewTests(APITestCase):
    """Test cases for Book Update View (PUT/PATCH /api/books/update/<id>/)"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.author = Author.objects.create(name="J.R.R. Tolkien")
        self.book = Book.objects.create(
            title="The Hobbit",
            publication_year=1937,
            author=self.author
        )
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_update_book_unauthenticated(self):
        """Test updating a book without authentication (should be rejected)"""
        update_data = {'title': 'Updated Title'}
        response = self.client.patch(f'/api/books/update/{self.book.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_book_authenticated_full_update(self):
        """Test full update (PUT) with authentication"""
        self.client.login(username='testuser', password='testpass123')
        
        update_data = {
            'title': 'The Hobbit Revised',
            'publication_year': 1937,
            'author': self.author.id
        }
        response = self.client.put(f'/api/books/update/{self.book.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify book was updated
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'The Hobbit Revised')
    
    def test_update_book_authenticated_partial_update(self):
        """Test partial update (PATCH) with authentication"""
        self.client.login(username='testuser', password='testpass123')
        
        update_data = {'title': 'The Hobbit - Special Edition'}
        response = self.client.patch(f'/api/books/update/{self.book.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify book was partially updated
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'The Hobbit - Special Edition')
        self.assertEqual(self.book.publication_year, 1937)  # Unchanged


class BookDeleteViewTests(APITestCase):
    """Test cases for Book Delete View (DELETE /api/books/delete/<id>/)"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.author = Author.objects.create(name="J.R.R. Tolkien")
        self.book = Book.objects.create(
            title="The Hobbit",
            publication_year=1937,
            author=self.author
        )
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_delete_book_unauthenticated(self):
        """Test deleting a book without authentication (should be rejected)"""
        response = self.client.delete(f'/api/books/delete/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify book still exists
        self.assertTrue(Book.objects.filter(id=self.book.id).exists())
    
    def test_delete_book_authenticated(self):
        """Test deleting a book with authentication (should be allowed)"""
        self.client.login(username='testuser', password='testpass123')
        
        book_id = self.book.id
        response = self.client.delete(f'/api/books/delete/{book_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify book was deleted
        self.assertFalse(Book.objects.filter(id=book_id).exists())
