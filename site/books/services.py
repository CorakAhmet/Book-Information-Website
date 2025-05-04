import requests
from datetime import datetime
from django.conf import settings

def search_google_books(query, max_results=10):
    """
    Google Books API ile kitap araması yapar
    """
    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": query,
        "maxResults": max_results,
        "printType": "books",
        "orderBy": "relevance"
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if 'items' not in data:
            return []
        
        books = []
        for item in data['items']:
            # Ana kitap detayları
            volume_info = item.get('volumeInfo', {})
            
            # Tarih formatını düzelt
            published_date = None
            if 'publishedDate' in volume_info:
                date_str = volume_info['publishedDate']
                try:
                    if len(date_str) == 4:  # Sadece yıl
                        published_date = datetime.strptime(date_str, "%Y").date()
                    elif len(date_str) == 7:  # Yıl-Ay
                        published_date = datetime.strptime(date_str, "%Y-%m").date()
                    else:  # Yıl-Ay-Gün
                        published_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    published_date = None
            
            # Kitap bilgilerini düzenle
            book = {
                'google_books_id': item.get('id'),
                'title': volume_info.get('title', 'İsimsiz'),
                'authors': volume_info.get('authors', ['Bilinmiyor']),
                'publisher': volume_info.get('publisher', ''),
                'published_date': published_date,
                'description': volume_info.get('description', ''),
                'page_count': volume_info.get('pageCount', 0),
                'categories': volume_info.get('categories', []),
                'language': volume_info.get('language', ''),
                'preview_link': volume_info.get('previewLink', ''),
                'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', '')
            }
            
            books.append(book)
        
        return books
    
    except requests.exceptions.RequestException as e:
        print(f"Google Books API hatası: {e}")
        return []

def get_book_details(google_books_id):
    """
    Belirli bir kitabın detaylarını Google Books API'den alır
    """
    url = f"https://www.googleapis.com/books/v1/volumes/{google_books_id}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if 'error' in data:
            return None
        
        volume_info = data.get('volumeInfo', {})
        
        # Tarih formatını düzelt
        published_date = None
        if 'publishedDate' in volume_info:
            date_str = volume_info['publishedDate']
            try:
                if len(date_str) == 4:  # Sadece yıl
                    published_date = datetime.strptime(date_str, "%Y").date()
                elif len(date_str) == 7:  # Yıl-Ay
                    published_date = datetime.strptime(date_str, "%Y-%m").date()
                else:  # Yıl-Ay-Gün
                    published_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                published_date = None
        
        # Kitap bilgilerini düzenle
        book = {
            'google_books_id': data.get('id'),
            'title': volume_info.get('title', 'İsimsiz'),
            'authors': volume_info.get('authors', ['Bilinmiyor']),
            'publisher': volume_info.get('publisher', ''),
            'published_date': published_date,
            'description': volume_info.get('description', ''),
            'page_count': volume_info.get('pageCount', 0),
            'categories': volume_info.get('categories', []),
            'language': volume_info.get('language', ''),
            'preview_link': volume_info.get('previewLink', ''),
            'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''),
            'isbn': [i['identifier'] for i in volume_info.get('industryIdentifiers', []) if i.get('type') == 'ISBN_13'],
            'average_rating': volume_info.get('averageRating', 0),
        }
        
        return book
    
    except requests.exceptions.RequestException as e:
        print(f"Google Books API hatası: {e}")
        return None 