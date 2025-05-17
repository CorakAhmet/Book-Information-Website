from django.contrib import admin
from .models import Book, Category, UserBook

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'rating', 'page_count', 'display_categories')
    list_filter = ('categories', 'rating', 'publication_date')
    search_fields = ('title', 'author', 'description')
    filter_horizontal = ('categories',)  # Kategorileri seçmek için daha kullanışlı arayüz
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'author', 'description', 'cover_image')
        }),
        ('Detaylar', {
            'fields': ('page_count', 'rating', 'publication_date', 'categories')
        }),
        ('Görünüm Özellikleri', {
            'fields': ('background_color', 'nav_tint_color'),
            'classes': ('collapse',),  # Bu kısım varsayılan olarak kapalı olacak
        }),
    )
    
    def display_categories(self, obj):
        """Kitabın kategorilerini virgülle ayrılmış olarak gösterir"""
        return ", ".join([category.name for category in obj.categories.all()])
    display_categories.short_description = 'Kategoriler'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'book_count')
    search_fields = ('name',)
    
    def book_count(self, obj):
        """Bu kategorideki kitap sayısını gösterir"""
        return obj.books.count()
    book_count.short_description = 'Kitap Sayısı'

class UserBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'completion', 'is_favorite', 'last_read')
    list_filter = ('is_favorite', 'completion')
    search_fields = ('user__username', 'book__title')
    raw_id_fields = ('user', 'book')  # Büyük tablolarda daha hızlı seçim yapma

admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserBook, UserBookAdmin) 