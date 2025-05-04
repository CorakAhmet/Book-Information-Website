from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Book, Category, UserLibrary
from .forms import AdvancedSearchForm
from .services import search_google_books, get_book_details
from django.core.files.base import ContentFile
import requests
from io import BytesIO
from datetime import datetime

def home(request):
    popular_books = Book.objects.all().order_by('-rating')[:4]
    new_books = Book.objects.all().order_by('-created_at')[:4]
    categories = Category.objects.all()
    
    context = {
        'popular_books': popular_books,
        'new_books': new_books,
        'categories': categories,
    }
    
    return render(request, 'books/home.html', context)

def book_list(request):
    books = Book.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    
    context = {
        'books': books,
        'categories': categories,
    }
    
    return render(request, 'books/book_list.html', context)

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    is_in_library = False
    
    if request.user.is_authenticated:
        is_in_library = UserLibrary.objects.filter(user=request.user, book=book).exists()
    
    # Benzer kitapları bul (aynı kategorideki diğer kitaplar)
    related_books = Book.objects.filter(categories__in=book.categories.all()).exclude(id=book.id).distinct()[:4]
    
    # Google Books'tan ek bilgileri getir (eğer Google Books ID varsa)
    google_book_info = None
    if book.google_books_id:
        google_book_info = get_book_details(book.google_books_id)
    
    context = {
        'book': book,
        'is_in_library': is_in_library,
        'related_books': related_books,
        'google_book_info': google_book_info,
    }
    
    return render(request, 'books/book_detail.html', context)

def category_books(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    books = Book.objects.filter(categories=category)
    
    context = {
        'category': category,
        'books': books,
    }
    
    return render(request, 'books/category_books.html', context)

def book_search(request):
    query = request.GET.get('q', '')
    books = []
    
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query) |
            Q(categories__name__icontains=query)
        ).distinct()
    
    context = {
        'query': query,
        'books': books,
    }
    
    return render(request, 'books/book_search.html', context)

def advanced_search(request):
    form = AdvancedSearchForm(request.GET or None)
    books = []
    google_books_results = []
    
    if request.GET:
        # Veritabanında ara
        query_filter = Q()
        
        if request.GET.get('q'):
            query = request.GET.get('q')
            query_filter |= (
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(description__icontains=query)
            )
        
        if request.GET.get('title'):
            query_filter &= Q(title__icontains=request.GET.get('title'))
        
        if request.GET.get('author'):
            query_filter &= Q(author__icontains=request.GET.get('author'))
        
        if request.GET.get('publisher'):
            query_filter &= Q(publisher__icontains=request.GET.get('publisher'))
        
        if request.GET.getlist('categories'):
            categories = request.GET.getlist('categories')
            query_filter &= Q(categories__id__in=categories)
        
        if request.GET.get('min_page'):
            query_filter &= Q(page_count__gte=int(request.GET.get('min_page')))
        
        if request.GET.get('max_page'):
            query_filter &= Q(page_count__lte=int(request.GET.get('max_page')))
        
        if request.GET.get('min_rating'):
            query_filter &= Q(rating__gte=float(request.GET.get('min_rating')))
        
        if request.GET.get('published_year'):
            year = int(request.GET.get('published_year'))
            query_filter &= Q(published_date__year=year)
        
        if query_filter:
            books = Book.objects.filter(query_filter).distinct()
        
        # Google Books'ta ara
        if request.GET.get('use_google_books') == 'on' and request.GET.get('q'):
            google_books_results = search_google_books(request.GET.get('q'))
    
    context = {
        'form': form,
        'books': books,
        'google_books_results': google_books_results,
        'is_search': bool(request.GET),
    }
    
    return render(request, 'books/advanced_search.html', context)

@login_required
def import_google_book(request, google_books_id):
    if request.method == 'POST':
        book_data = get_book_details(google_books_id)
        
        if not book_data:
            messages.error(request, "Kitap bilgileri alınamadı.")
            return redirect('advanced_search')
        
        # Kitap zaten var mı kontrol et
        if Book.objects.filter(google_books_id=google_books_id).exists():
            messages.info(request, f'"{book_data["title"]}" kitabı zaten veritabanında mevcut.')
            book = Book.objects.get(google_books_id=google_books_id)
            return redirect('book_detail', book_id=book.id)
        
        # Kategorileri bul veya oluştur
        categories = []
        for category_name in book_data.get('categories', []):
            category, created = Category.objects.get_or_create(name=category_name)
            categories.append(category)
        
        # Kitabı oluştur
        book = Book(
            title=book_data['title'],
            author=', '.join(book_data['authors']),
            description=book_data.get('description', ''),
            page_count=book_data.get('page_count', 0),
            language=book_data.get('language', ''),
            publisher=book_data.get('publisher', ''),
            published_date=book_data.get('published_date'),
            rating=book_data.get('average_rating', 5.0),  # Default değer
            google_books_id=google_books_id,
        )
        
        # Kapak resmi URL'sini kullan
        if book_data.get('thumbnail'):
            book.cover_image_url = book_data['thumbnail']
        else:
            # Default kapak resmi
            dummy_image = ContentFile(b'dummy-image', name=f'dummy-{google_books_id}.jpg')
            book.cover_image = dummy_image
        
        book.save()
        
        # Kategorileri ekle
        for category in categories:
            book.categories.add(category)
        
        messages.success(request, f'"{book.title}" kitabı başarıyla içe aktarıldı.')
        return redirect('book_detail', book_id=book.id)
    
    return redirect('advanced_search')

@login_required
def user_library(request):
    user_books = UserLibrary.objects.filter(user=request.user).order_by('-added_at')
    
    context = {
        'user_books': user_books,
    }
    
    return render(request, 'books/user_library.html', context)

@login_required
def add_to_library(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        # Eğer kitap zaten kütüphanede varsa, tekrar ekleme
        if not UserLibrary.objects.filter(user=request.user, book=book).exists():
            UserLibrary.objects.create(user=request.user, book=book)
            messages.success(request, f'"{book.title}" kitabı kütüphanenize eklendi.')
        else:
            messages.info(request, f'"{book.title}" kitabı zaten kütüphanenizde.')
    
    return redirect('book_detail', book_id=book.id)

@login_required
def remove_from_library(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        user_book = UserLibrary.objects.filter(user=request.user, book=book)
        if user_book.exists():
            user_book.delete()
            messages.success(request, f'"{book.title}" kitabı kütüphanenizden çıkarıldı.')
        else:
            messages.error(request, 'Bu kitap kütüphanenizde bulunamadı.')
    
    return redirect('book_detail', book_id=book.id)
