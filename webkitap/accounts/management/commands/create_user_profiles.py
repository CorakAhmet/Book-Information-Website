from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Profili olmayan kullanıcılar için profil oluşturur'

    def handle(self, *args, **options):
        users_without_profile = []
        total_users = User.objects.count()
        
        # Profili olmayan kullanıcıları bul
        for user in User.objects.all():
            try:
                # Profilin zaten var mı kontrol et
                user.profile
            except User.profile.RelatedObjectDoesNotExist:
                # Profil yoksa, listeye ekle
                users_without_profile.append(user)
        
        # Profil oluştur
        for user in users_without_profile:
            UserProfile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f"Profil oluşturuldu: {user.username}"))
        
        self.stdout.write(
            self.style.SUCCESS(
                f"İşlem tamamlandı. Toplam {total_users} kullanıcıdan {len(users_without_profile)} tanesine profil oluşturuldu."
            )
        ) 