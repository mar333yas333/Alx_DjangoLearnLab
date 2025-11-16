"""
Bookshelf Views with Security Best Practices

All views implement:
- Permission-based access control
- CSRF protection (via {% csrf_token %} in templates)
- Input validation using Django Forms
- ORM-based queries (protection against SQL Injection)
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import SearchForm
from .forms import ExampleForm


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Display list of all books with secure search functionality.
    """
    books = Book.objects.all()
    form = SearchForm(request.GET or None)

    if form.is_valid():
        query = form.cleaned_data['query']
        books = books.filter(title__icontains=query)

    return render(request, 'bookshelf/book_list.html', {'books': books, 'form': form})


@permission_required('bookshelf.can_create', raise_exception=True)
def secure_create_book(request):
    """Create a new book securely using form validation."""
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            if query.strip():
                Book.objects.create(title=query)
                return redirect('book_list')
    else:
        form = SearchForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})


@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            book.title = form.cleaned_data['query']
            book.save()
            return redirect('book_list')
    else:
        form = SearchForm(initial={'query': book.title})
    return render(request, 'bookshelf/edit_book.html', {'book': book, 'form': form})


@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/delete_book.html', {'book': book})
