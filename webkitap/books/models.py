from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='covers/')
    page_count = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    publication_date = models.DateField(null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    background_color = models.CharField(max_length=30, default="rgba(240,240,232,0.9)")
    nav_tint_color = models.CharField(max_length=30, default="#000")
    
    def __str__(self):
        return self.title

class UserBook(models.Model):
    READING_STATUS_CHOICES = [
        ('want_to_read', 'Okuyacağım'),
        ('reading', 'Okuyorum'),
        ('read', 'Okudum'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='user_books')
    completion = models.IntegerField(default=0)  # 0-100 arası tamamlanma yüzdesi
    is_favorite = models.BooleanField(default=False)
    last_read = models.DateTimeField(auto_now=True)
    reading_status = models.CharField(max_length=20, choices=READING_STATUS_CHOICES, default='want_to_read')
    
    # Okuma hedefleri için
    reading_goal_daily = models.IntegerField(default=0, help_text="Günlük sayfa hedefi")
    start_date = models.DateField(null=True, blank=True)
    finish_date = models.DateField(null=True, blank=True)
    
    # Okuma istatistikleri
    total_reading_time = models.IntegerField(default=0, help_text="Toplam okuma süresi (dakika)")
    
    class Meta:
        unique_together = ('user', 'book')
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

# Okuma İstatistikleri için yeni model
class ReadingSession(models.Model):
    user_book = models.ForeignKey(UserBook, on_delete=models.CASCADE, related_name='reading_sessions')
    date = models.DateField(auto_now_add=True)
    duration = models.IntegerField(help_text="Okuma süresi (dakika)")
    pages_read = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user_book.user.username} - {self.user_book.book.title} - {self.date}"

# Okuma Hedefleri için model
class ReadingGoal(models.Model):
    PERIOD_CHOICES = [
        ('daily', 'Günlük'),
        ('weekly', 'Haftalık'),
        ('monthly', 'Aylık'),
        ('yearly', 'Yıllık'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_goals')
    target_books = models.IntegerField(default=0)
    target_pages = models.IntegerField(default=0)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_period_display()} Hedef" 