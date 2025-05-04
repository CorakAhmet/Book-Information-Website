from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Profil zaten sinyal ile oluşturulacak
            messages.success(request, f'Hesabınız başarıyla oluşturuldu. Şimdi giriş yapabilirsiniz.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile
    
    if request.method == 'POST':
        # Kullanıcı güncellemesi
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        
        # Profil güncellemesi
        profile.bio = request.POST.get('bio', '')
        
        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']
        
        profile.save()
        
        messages.success(request, 'Profiliniz başarıyla güncellendi.')
        return redirect('profile')
    
    return render(request, 'accounts/edit_profile.html')
