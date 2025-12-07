from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer for serializing Book model instances.
    
    Fields:
    - id: Auto-generated primary key (read-only).
    - title: CharField for the book's title.
    - publication_year: IntegerField for the year the book was published.
    - author: PrimaryKeyRelatedField linking to the Author model.
    
    Custom Validation:
    - publication_year: Custom validate_publication_year() ensures the year is not in the future.
                        This prevents creation or update of books with future publication dates.
    
    Usage:
    - Used standalone to serialize individual Book instances.
    - Also used as a nested serializer in AuthorSerializer to serialize related books for an author.
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        Ensures that the publication year is not in the future.
        
        Args:
            value: The publication year value being validated.
        
        Raises:
            serializers.ValidationError: If the publication year is greater than the current year.
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer for serializing Author model instances with nested Book data.
    
    Fields:
    - id: Auto-generated primary key (read-only).
    - name: CharField for the author's name.
    - books: Nested BookSerializer (many=True, read-only) that serializes all related books.
    
    Nested Relationship:
    - The 'books' field uses the related_name='books' defined in the Book.author ForeignKey.
    - This field is read-only and uses the BookSerializer to serialize each related book.
    - When an Author is serialized, all of its related Books are automatically included in the response.
    
    Usage:
    - Used to serialize Author instances with full nested book data.
    - Allows clients to retrieve complete author information including all their books in a single request.
    """
    
    # Nested serializer for related books
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
