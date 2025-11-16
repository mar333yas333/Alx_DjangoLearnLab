from django.urls import path
from .views import list_books, LibraryDetailView
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('books/', list_books, name='list_books'),
    # Book create/edit/delete (secured by permission_required in views)
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/int:pk/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='book_delete'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # auth URLs
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),
]
