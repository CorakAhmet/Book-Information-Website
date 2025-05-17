from django.core.management.base import BaseCommand
from books.models import UserBook, ReadingGoal
from accounts.utils import create_reading_reminder, create_goal_notification
from django.utils import timezone
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Kullanıcılara bildirimler gönderir: okuma hatırlatıcıları ve hedef bilgilendirmeleri'

    def handle(self, *args, **options):
        self.stdout.write('Bildirimler gönderiliyor...')
        
        # Okuma hatırlatıcıları
        for user_book in UserBook.objects.filter(reading_status='reading'):
            notification = create_reading_reminder(user_book)
            if notification:
                self.stdout.write(self.style.SUCCESS(
                    f"{user_book.user.username} kullanıcısına '{user_book.book.title}' için okuma hatırlatıcısı gönderildi."
                ))
        
        # Hedef bildirimleri
        for user in User.objects.all():
            goals = ReadingGoal.objects.filter(user=user, is_completed=False)
            for goal in goals:
                notification = create_goal_notification(user, goal)
                if notification:
                    self.stdout.write(self.style.SUCCESS(
                        f"{user.username} kullanıcısına okuma hedefi hatırlatıcısı gönderildi."
                    ))
        
        self.stdout.write(self.style.SUCCESS('Bildirim gönderme tamamlandı.')) 