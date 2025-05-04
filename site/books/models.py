from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    
    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Kitap Adı")
    author = models.CharField(max_length=100, verbose_name="Yazar")
    description = models.TextField(verbose_name="Açıklama")
    page_count = models.IntegerField(verbose_name="Sayfa Sayısı")
    language = models.CharField(max_length=50, verbose_name="Dil")
    publisher = models.CharField(max_length=100, blank=True, null=True, verbose_name="Yayınevi")
    published_date = models.DateField(blank=True, null=True, verbose_name="Yayın Tarihi")
    rating = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="Puan")
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name="Kapak Resmi")
    cover_image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Kapak Resmi URL")
    categories = models.ManyToManyField(Category, verbose_name="Kategoriler")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    google_books_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Google Books ID")
    
    class Meta:
        verbose_name = "Kitap"
        verbose_name_plural = "Kitaplar"
    
    def __str__(self):
        return self.title

    def get_cover_image(self):
        """Kapak resmi URL'sini veya yüklenen resmi döndürür"""
        if self.cover_image_url:
            return self.cover_image_url
        elif self.cover_image:
            return self.cover_image.url
        return None

class UserLibrary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Kitap")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    completion = models.IntegerField(default=0, verbose_name="Tamamlanma Yüzdesi")
    last_read = models.DateTimeField(null=True, blank=True, verbose_name="Son Okunma Tarihi")
    
    class Meta:
        verbose_name = "Kullanıcı Kütüphanesi"
        verbose_name_plural = "Kullanıcı Kütüphaneleri"
        unique_together = ('user', 'book')
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
