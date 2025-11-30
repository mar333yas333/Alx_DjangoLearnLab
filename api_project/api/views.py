from rest_framework import generics, viewsets, permissions
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """API endpoint that returns a list of all books."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookViewSet(viewsets.ModelViewSet):
    """ViewSet providing CRUD operations for Book."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
