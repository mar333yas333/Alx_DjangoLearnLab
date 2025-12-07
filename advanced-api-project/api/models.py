from django.db import models


class Author(models.Model):
    """
    Author model representing book authors.
    
    Fields:
    - name: A CharField storing the author's name. This is the primary identifier for an author.
    
    Relationship:
    - One Author can have multiple Books (one-to-many relationship via Book.author FK).
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Book(models.Model):
    """
    Book model representing published books.
    
    Fields:
    - title: A CharField for the book's title.
    - publication_year: An IntegerField for the year the book was published.
    - author: A ForeignKey to the Author model, establishing a one-to-many relationship.
              Deleting an author will cascade-delete all associated books.
    
    Relationship:
    - Many Books can belong to one Author (many-to-one via FK).
    - The AuthorSerializer includes a nested BookSerializer to serialize all related books.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
