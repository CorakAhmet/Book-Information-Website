from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from .models import Book, Category, UserBook, ReadingSession, ReadingGoal
from django import forms
from accounts.utils import create_notification

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'cover_image', 'page_count', 
                  'rating', 'publication_date', 'categories']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

def home(request):
    categories = Category.objects.all()
    popular_books = Book.objects.order_by('-rating')[:5]
    new_books = Book.objects.order_by('-created_at')[:5]
    bestseller_books = Book.objects.order_by('-rating')[:5]  # Örnek olarak, gerçekte farklı olabilir
    
    context = {
        'categories': categories,
        'popular_books': popular_books,
        'new_books': new_books,
        'bestseller_books': bestseller_books
    }
    return render(request, 'books/home.html', context)

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    is_in_library = False
    user_book = None
    reading_sessions = None
    
    if request.user.is_authenticated:
        user_book = UserBook.objects.filter(user=request.user, book=book).first()
        is_in_library = user_book is not None
        
        if is_in_library:
            reading_sessions = ReadingSession.objects.filter(user_book=user_book)
    
    context = {
        'book': book,
        'is_in_library': is_in_library,
        'user_book': user_book,
        'reading_sessions': reading_sessions
    }
    return render(request, 'books/book_detail.html', context)

def search(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(
        Q(title__icontains=query) | 
        Q(author__icontains=query) | 
        Q(description__icontains=query)
    ).distinct() if query else Book.objects.none()
    
    context = {
        'books': books,
        'query': query
    }
    return render(request, 'books/search.html', context)

def category_books(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    books = category.books.all()
    
    context = {
        'category': category,
        'books': books
    }
    return render(request, 'books/category_books.html', context)

@login_required
def library(request):
    user_books = UserBook.objects.filter(user=request.user)
    
    context = {
        'user_books': user_books
    }
    return render(request, 'books/library.html', context)

@login_required
def add_to_library(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user_book, created = UserBook.objects.get_or_create(user=request.user, book=book)
    
    return redirect('book_detail', book_id=book_id)

@login_required
def remove_from_library(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    UserBook.objects.filter(user=request.user, book=book).delete()
    
    return redirect('book_detail', book_id=book_id)

def about(request):
    return render(request, 'books/about.html')

@staff_member_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            # Sabit görünüm değerleri ayarla
            book.background_color = "rgba(240,240,232,0.9)"
            book.nav_tint_color = "#000"
            book.save()
            form.save_m2m()  # ManyToMany ilişkileri kaydet
            messages.success(request, f'"{book.title}" başarıyla eklendi!')
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookForm()
    
    context = {
        'form': form,
        'categories': Category.objects.all(),
        'form_title': 'Kitap Ekle',
        'is_edit': False
    }
    return render(request, 'books/book_form.html', context)

@staff_member_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            # Görünüm ayarlarını koruyalım
            book.save()
            form.save_m2m()  # ManyToMany ilişkileri kaydet
            messages.success(request, f'"{book.title}" başarıyla güncellendi!')
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookForm(instance=book)
    
    context = {
        'form': form,
        'categories': Category.objects.all(),
        'form_title': 'Kitap Düzenle',
        'is_edit': True,
        'book': book
    }
    return render(request, 'books/book_form.html', context)

@staff_member_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            
            # Ajax isteği ise JSON yanıtı dön
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'id': category.id,
                    'name': category.name
                })
            
            messages.success(request, f'"{category.name}" kategorisi başarıyla eklendi!')
            return redirect('add_book')
    else:
        form = CategoryForm()
    
    context = {
        'form': form
    }
    return render(request, 'books/add_category.html', context)

@login_required
def update_reading_status(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        user_book, created = UserBook.objects.get_or_create(user=request.user, book=book)
        
        status = request.POST.get('reading_status')
        if status in [choice[0] for choice in UserBook.READING_STATUS_CHOICES]:
            user_book.reading_status = status
            user_book.save()
            messages.success(request, f'Okuma durumu güncellendi!')
        
        return redirect('book_detail', book_id=book_id)
    
    return redirect('book_detail', book_id=book_id)

@login_required
def record_reading_session(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        user_book = get_object_or_404(UserBook, user=request.user, book=book)
        
        duration = request.POST.get('duration', 0)
        pages_read = request.POST.get('pages_read', 0)
        notes = request.POST.get('notes', '')
        
        # Okuma seansı oluştur
        ReadingSession.objects.create(
            user_book=user_book,
            duration=duration,
            pages_read=pages_read,
            notes=notes
        )
        
        # Kullanıcının toplam okuma süresini güncelle
        user_book.total_reading_time += int(duration)
        
        # Tamamlanma yüzdesini güncelle
        pages_read_int = int(pages_read)
        if book.page_count > 0:
            new_completion = min(100, int((pages_read_int / book.page_count) * 100))
            user_book.completion = new_completion
            
            # Eğer %100 tamamlandıysa, okuma durumunu "okudum" olarak işaretle
            if new_completion == 100:
                user_book.reading_status = 'read'
                
        user_book.save()
        
        messages.success(request, f'Okuma seansı kaydedildi!')
        return redirect('book_detail', book_id=book_id)
    
    return redirect('book_detail', book_id=book_id)

@login_required
def reading_stats(request):
    # Kullanıcının kitaplarını ve okuma istatistiklerini getir
    user_books = UserBook.objects.filter(user=request.user)
    reading_sessions = ReadingSession.objects.filter(user_book__user=request.user)
    reading_goals = ReadingGoal.objects.filter(user=request.user)
    
    # Okunan toplam kitap sayısı
    books_read = user_books.filter(reading_status='read').count()
    
    # Okumakta olduğu kitaplar
    books_reading = user_books.filter(reading_status='reading')
    
    # Okuyacağı kitaplar
    books_to_read = user_books.filter(reading_status='want_to_read')
    
    # Toplam okuma süresi (dakika)
    total_reading_time = sum(ub.total_reading_time for ub in user_books)
    
    # Toplam okunan sayfa
    total_pages_read = sum(rs.pages_read for rs in reading_sessions)
    
    context = {
        'books_read': books_read,
        'books_reading': books_reading,
        'books_to_read': books_to_read,
        'total_reading_time': total_reading_time,
        'total_pages_read': total_pages_read,
        'reading_sessions': reading_sessions,
        'reading_goals': reading_goals
    }
    return render(request, 'books/reading_stats.html', context)

@login_required
def set_reading_goal(request):
    if request.method == 'POST':
        target_books = request.POST.get('target_books', 0)
        target_pages = request.POST.get('target_pages', 0)
        period = request.POST.get('period')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        if period in [choice[0] for choice in ReadingGoal.PERIOD_CHOICES]:
            ReadingGoal.objects.create(
                user=request.user,
                target_books=target_books,
                target_pages=target_pages,
                period=period,
                start_date=start_date,
                end_date=end_date
            )
            messages.success(request, f'Okuma hedefi oluşturuldu!')
            return redirect('reading_stats')
    
    return render(request, 'books/set_reading_goal.html', {
        'period_choices': ReadingGoal.PERIOD_CHOICES
    })

@login_required
def recommended_books(request):
    """Kullanıcıya özel kitap önerileri sunar"""
    # Kullanıcının okuduğu kitaplar
    user_read_books = UserBook.objects.filter(
        user=request.user, 
        reading_status='read'
    ).values_list('book__id', flat=True)
    
    # Okunan kitaplardan kategorileri belirle
    user_categories = Category.objects.filter(
        books__id__in=user_read_books
    ).distinct()
    
    # Bu kategorilere ait, kullanıcının okumadığı kitaplar
    recommended = Book.objects.filter(
        categories__in=user_categories
    ).exclude(
        id__in=user_read_books
    ).exclude(
        id__in=UserBook.objects.filter(user=request.user).values_list('book__id', flat=True)
    ).distinct().order_by('-rating')[:10]
    
    context = {
        'recommended_books': recommended
    }
    return render(request, 'books/recommended_books.html', context)

@login_required
def send_book_recommendation(request):
    """Kullanıcıya kitap önerilerini bildirim olarak gönderir"""
    # Kullanıcının okuduğu kitaplar
    user_read_books = UserBook.objects.filter(
        user=request.user, 
        reading_status='read'
    ).values_list('book__id', flat=True)
    
    # Okunan kitaplardan kategorileri belirle
    user_categories = Category.objects.filter(
        books__id__in=user_read_books
    ).distinct()
    
    # Bu kategorilere ait, kullanıcının okumadığı, yüksek puanlı 1 kitap
    if user_categories.exists():
        top_book = Book.objects.filter(
            categories__in=user_categories
        ).exclude(
            id__in=UserBook.objects.filter(user=request.user).values_list('book__id', flat=True)
        ).distinct().order_by('-rating').first()
        
        if top_book:
            # Bildirim gönder
            create_notification(
                user=request.user,
                notification_type='book_recommendation',
                title='Sizin İçin Kitap Önerisi',
                message=f'Beğenebileceğinizi düşündüğümüz bir kitap: {top_book.title} - {top_book.author}',
                link=f'/books/{top_book.id}/'
            )
            messages.success(request, 'Kitap önerisi bildirim olarak gönderildi!')
        else:
            messages.info(request, 'Şu an için size önerecek yeni bir kitap bulamadık.')
    else:
        messages.info(request, 'Öneriler için önce bir kitap okumanız gerekiyor.')
    
    return redirect('recommended_books') 