# Kitaplarım - Web Uygulaması

Kitaplarım, kullanıcıların kitapları keşfedebileceği, kütüphanelerine ekleyebileceği ve okuma alışkanlıklarını takip edebileceği bir web uygulamasıdır. Bu proje, bir React Native mobil uygulamasının web versiyonudur.

## Özellikler

- Kitapları keşfetme ve arama
- Kitap detaylarını görüntüleme
- Kütüphane oluşturma ve yönetme
- Kullanıcı profili ve hesap yönetimi
- Kategorilere göre kitapları filtreleme

## Teknolojiler

- **Backend**: Django
- **Veritabanı**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript (jQuery)
- **CSS Framework**: Bootstrap 5

## Kurulum

### Ön Gereksinimler

- Python 3.8 veya üzeri
- PostgreSQL
- Pip (Python paket yöneticisi)

### Adımlar

1. Projeyi klonla:
   ```
   git clone <repo-url>
   cd webkitap
   ```

2. Sanal ortam oluştur ve aktifleştir:
   ```
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. Gerekli paketleri yükle:
   ```
   pip install -r requirements.txt
   ```

4. PostgreSQL veritabanı oluştur:
   ```
   createdb kitaplarim
   ```

5. Veritabanı ayarlarını `kitaplarim/settings.py` dosyasında yapılandır.

6. Veritabanı tablolarını oluştur:
   ```
   python manage.py migrate
   ```

7. Statik dosyaları topla:
   ```
   python manage.py collectstatic
   ```

8. Admin kullanıcısı oluştur:
   ```
   python manage.py createsuperuser
   ```

9. Sunucuyu başlat:
   ```
   python manage.py runserver
   ```

10. Tarayıcında şu adrese git: `http://127.0.0.1:8000/`

## Yönetim Arayüzü

Admin paneline erişmek için: `http://127.0.0.1:8000/admin/`

## Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır. 