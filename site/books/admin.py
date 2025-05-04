from django.contrib import admin
from .models import Category, Book, UserLibrary

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'rating', 'page_count')
    list_filter = ('categories', 'rating')
    search_fields = ('title', 'author', 'description')
    filter_horizontal = ('categories',)

@admin.register(UserLibrary)
class UserLibraryAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'completion', 'added_at', 'last_read')
    list_filter = ('user', 'completion')
    search_fields = ('user__username', 'book__title')
