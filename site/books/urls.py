from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('books/search/', views.book_search, name='book_search'),
    path('books/advanced-search/', views.advanced_search, name='advanced_search'),
    path('books/import-google-book/<str:google_books_id>/', views.import_google_book, name='import_google_book'),
    path('library/', views.user_library, name='user_library'),
    path('library/add/<int:book_id>/', views.add_to_library, name='add_to_library'),
    path('library/remove/<int:book_id>/', views.remove_from_library, name='remove_from_library'),
    path('categories/<int:category_id>/', views.category_books, name='category_books'),
] 