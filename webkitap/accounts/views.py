from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import UserProfile, Notification
from django import forms
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import JsonResponse

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'bio']

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hesabınız oluşturuldu! Şimdi giriş yapabilirsiniz.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profiliniz güncellendi!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/edit_profile.html', context)

def custom_logout(request):
    """Özel logout fonksiyonu - GET metodu ile çalışır"""
    logout(request)
    return redirect('home')  # Ana sayfaya yönlendir

@login_required
def notifications(request):
    """Kullanıcının bildirimlerini göster ve okundu olarak işaretleme"""
    user_notifications = request.user.notifications.all()
    
    context = {
        'notifications': user_notifications
    }
    return render(request, 'accounts/notifications.html', context)

@login_required
def mark_notification_read(request, notification_id):
    """Bildirimi okundu olarak işaretle"""
    notification = Notification.objects.get(id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    
    return redirect('notifications')

@login_required
def delete_notification(request, notification_id):
    """Bildirimi sil"""
    notification = Notification.objects.get(id=notification_id, user=request.user)
    notification.delete()
    messages.success(request, "Bildirim silindi.")
    
    return redirect('notifications')

@login_required
def mark_all_read(request):
    """Tüm bildirimleri okundu olarak işaretle"""
    Notification.objects.filter(user=request.user).update(is_read=True)
    messages.success(request, "Tüm bildirimler okundu olarak işaretlendi.")
    
    return redirect('notifications')

@login_required
def theme_switch(request):
    """Tema değiştirme görünümü"""
    if request.method == 'POST':
        theme = request.POST.get('theme')
        
        if theme in ['light', 'dark']:
            try:
                profile = request.user.profile
            except:
                # Eğer kullanıcının profili yoksa oluştur
                from .models import UserProfile
                profile = UserProfile.objects.create(user=request.user)
                
            # Kullanıcının tema tercihini güncelle
            profile.theme_preference = theme
            profile.save()
            
            # AJAX isteği ise JSON yanıtı dön
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'theme': theme})
                
            # Normal form gönderimi ise mesaj ekle
            messages.success(request, "Tema değişikliği başarıyla uygulandı.")
        
    # HTTP_REFERER başlığını kontrol et ve kullanıcıyı geri yönlendir
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('home')  # Varsayılan olarak ana sayfaya yönlendir 