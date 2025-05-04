from django import forms
from .models import Category

class AdvancedSearchForm(forms.Form):
    q = forms.CharField(
        label="Arama Terimi", 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kitap adı, yazar, konu...'}),
    )
    
    title = forms.CharField(
        label="Kitap Adı", 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kitap adı...'}),
    )
    
    author = forms.CharField(
        label="Yazar", 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Yazar adı...'}),
    )
    
    publisher = forms.CharField(
        label="Yayınevi", 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Yayınevi...'}),
    )
    
    categories = forms.ModelMultipleChoiceField(
        label="Kategoriler",
        queryset=Category.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
    )
    
    min_page = forms.IntegerField(
        label="Minimum Sayfa Sayısı", 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
    )
    
    max_page = forms.IntegerField(
        label="Maksimum Sayfa Sayısı", 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
    )
    
    min_rating = forms.DecimalField(
        label="Minimum Puan", 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10', 'step': '0.1'}),
    )
    
    published_year = forms.IntegerField(
        label="Yayın Yılı", 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Örn: 2022'}),
    )
    
    use_google_books = forms.BooleanField(
        label="Google Books'ta da Ara", 
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    ) 