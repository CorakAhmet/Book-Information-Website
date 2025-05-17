from .models import Notification
from django.utils import timezone
import datetime

def create_notification(user, notification_type, title, message, link=None):
    """
    Kullanıcı için bildirim oluşturur.
    
    Args:
        user: Bildirimin gönderileceği kullanıcı
        notification_type: Bildirim tipi ('reading_goal', 'system', 'book_recommendation', 'reminder')
        title: Bildirim başlığı
        message: Bildirim içeriği
        link: Bildirime tıklandığında yönlendirilecek bağlantı (opsiyonel)
    
    Returns:
        Oluşturulan bildirim nesnesi
    """
    notification = Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        link=link
    )
    return notification

def create_reading_reminder(user_book):
    """
    Kullanıcıya okuma hatırlatması gönderir.
    
    Args:
        user_book: Hatırlatma yapılacak UserBook nesnesi
    """
    # Son okuma tarihi 3 günden eski ise hatırlatma gönder
    last_read = user_book.last_read.date()
    today = timezone.now().date()
    days_since_last_read = (today - last_read).days
    
    if days_since_last_read >= 3 and user_book.reading_status == 'reading':
        title = "Okuma Hatırlatıcısı"
        message = f"'{user_book.book.title}' kitabını {days_since_last_read} gündür okumadınız. Okumaya devam etmek ister misiniz?"
        link = f"/books/{user_book.book.id}/"
        
        return create_notification(
            user=user_book.user,
            notification_type='reminder',
            title=title,
            message=message,
            link=link
        )
    return None

def create_goal_notification(user, reading_goal):
    """
    Okuma hedefi için bildirim oluşturur.
    
    Args:
        user: Hedef sahibi kullanıcı
        reading_goal: ReadingGoal nesnesi
    """
    title = "Okuma Hedefi"
    today = timezone.now().date()
    remaining_days = (reading_goal.end_date - today).days
    
    if remaining_days <= 7 and remaining_days > 0 and not reading_goal.is_completed:
        message = f"{reading_goal.get_period_display()} okuma hedefinizi tamamlamak için {remaining_days} gününüz kaldı."
        link = "/reading_stats/"
        
        return create_notification(
            user=user,
            notification_type='reading_goal',
            title=title,
            message=message,
            link=link
        )
    return None 