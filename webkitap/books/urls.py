from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('search/', views.search, name='search'),
    path('category/<int:category_id>/', views.category_books, name='category_books'),
    path('library/', views.library, name='library'),
    path('add-to-library/<int:book_id>/', views.add_to_library, name='add_to_library'),
    path('remove-from-library/<int:book_id>/', views.remove_from_library, name='remove_from_library'),
    path('about/', views.about, name='about'),
    path('add-book/', views.add_book, name='add_book'),
    path('edit-book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('add-category/', views.add_category, name='add_category'),
    path('reading-status/<int:book_id>/', views.update_reading_status, name='update_reading_status'),
    path('reading-session/<int:book_id>/', views.record_reading_session, name='record_reading_session'),
    path('reading-stats/', views.reading_stats, name='reading_stats'),
    path('set-reading-goal/', views.set_reading_goal, name='set_reading_goal'),
    # Kitap önerileri URL'leri
    path('recommended-books/', views.recommended_books, name='recommended_books'),
    path('send-book-recommendation/', views.send_book_recommendation, name='send_book_recommendation'),
] 