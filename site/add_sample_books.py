import os
import django

# Django ortamını başlat
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kitapsite.settings')
django.setup()

from books.models import Book, Category
from django.core.files.images import ImageFile
from django.core.files.base import ContentFile

def add_categories():
    # Kategorileri oluştur
    categories = [
        "Roman",
        "Bilim",
        "Kişisel Gelişim",
        "Tarih",
        "Macera",
        "Drama",
        "Eğitim",
    ]
    
    created_categories = []
    for category_name in categories:
        category, created = Category.objects.get_or_create(name=category_name)
        created_categories.append(category)
        print(f"Kategori {'oluşturuldu' if created else 'zaten vardı'}: {category_name}")
    
    return created_categories

def add_books(categories):
    # Kitapları oluştur
    books_data = [
        {
            "title": "Hayvan Çiftliği",
            "author": "George Orwell",
            "description": "İngiliz yazar George Orwell (1903-1950), ülkemizde daha çok Bindokuzyüzseksendört adlı kitabıyla tanınır. Hayvan Çiftliği, onun çağdaş klasikler arasına girmiş ikinci ünlü yapıtıdır. 1940'lardaki 'reel sosyalizm'in eleştirisi olan bu roman, dünya edebiyatında 'yergi' türünün başyapıtlarından biridir. Hayvan Çiftliği'nin kişileri hayvanlardır. Bir çiftlikte yaşayan hayvanlar, kendilerini sömüren insanlara başkaldırıp çiftliğin yönetimini ele geçirirler. Amaçları daha eşitlikçi bir topluluk oluşturmaktır. Aralarında en akıllı olanlar domuzlar; kısa sürede önder bir takım oluştururlar, devrimi de onlar yolundan saptırırlar. Ne yazık ki insanlardan daha baskıcı, daha acımasız bir diktatörlük kurulmuştur artık. George Orwell, bu romanında tarihsel bir gerçeği eleştirmektedir. Romandaki önder domuzun, düpedüz Stalin'i simgelediği açıkça görülecektir. Öbür kişiler bire bir belli olmasalar da, bir diktatörlük ortamındna olabilecek kişilerdir. Romanın alt başlığı Bir Peri Masalı'dır. Küçükleri eğlendirecek bir peri masalı değildir; ama roman, bir masal anlatımıyla yazılmıştır.",
            "page_count": 152,
            "language": "Türkçe",
            "rating": 4.4,
            "categories": ["Roman", "Drama"],
        },
        {
            "title": "Üç Cisim Problemi",
            "author": "Cixin Liu",
            "description": "Bilim kurgu türünde bir roman olup, Çinli yazar Liu Cixin tarafından kaleme alınmıştır. Hikaye, bir bilim kadınının Çin'den günümüzdeki dünyaya geçiş yapmasını ve insanlığın, dünya dışı varlıklarla karşı karşıya gelmesini anlatır. İki farklı gezegen arasında kurulan bir iletişim köprüsü ve bu köprü üzerinden gelen mesajlarla başlayan olaylar, romanın temelini oluşturur. Roman, bilimsel kavramlarla dolu karmaşık bir kurguya sahiptir ve okuyuculara bilim kurgu macerasının yanı sıra insan doğası, teknolojinin etkileri ve evrensel sorunlar üzerine düşündürücü sorular da sunar.",
            "page_count": 416,
            "language": "Türkçe",
            "rating": 3.5,
            "categories": ["Bilim", "Macera", "Roman"],
        },
        {
            "title": "Ustalık",
            "author": "Robert Greene",
            "description": "Herkesin nasıl olduğuna bakmaksızın, sahip olduğu karaktere uygun bir yaşam sürmesine izin vermelisiniz ve değiştirmeye çabalamak ya da lanetlemek yerine bu karakterinden doğasının izin verdiği biçimde yararlanmalısınız. Yaşayın ve bırakın yaşasınlar atasözünün gerçek anlamı budur... İnsanların davranışlarına öfkelenmek, yolunuza yuvarlandığı için bir taşa kızmak kadar saçmadır. Çoğu insan açısından yapabileceğimiz en akılcı davranış, değiştiremeyeceklerinizden yararlanmaya karar vermek.",
            "page_count": 416,
            "language": "Türkçe",
            "rating": 4.7,
            "categories": ["Kişisel Gelişim", "Eğitim"],
        },
        {
            "title": "Dünya Tarihi 101",
            "author": "Tom Head",
            "description": "Tarih şaşırtıcı olaylar, güçlü liderler, entrikalar ve ilginç keşiflerle dolu binlerce yıllık bir maceradır. Buna rağmen tarih kitapları çoğunlukla tekdüze, sıkıcı ve eğlenceli olmaktan alabildiğine uzaktır. Dünya Tarihi 101 ise bütün bu sıkıcı detayları bir kenara bırakıyor ve sizi uygarlık tarihine doğru büyüleyici bir yolculuğa çıkarıyor.",
            "page_count": 248,
            "language": "Türkçe",
            "rating": 7.2,
            "categories": ["Tarih", "Bilim"],
        },
        {
            "title": "Momo",
            "author": "Michael Ende",
            "description": "Momo, yoksul ama bir o kadar da zengin bir kızdır. Saçları kıvır kıvır ve kapkaradır. Simsiyah, kocaman, güzel gözleri vardır... Zamanın hırsızlarını alt etmek için Momo'nun erdemli yüreğinden, usta bir bilgenin öğütlerinden ve insanların aklının erişemeyeceği olağanüstü, gizemli güçlerden başka bir şey gerekmez...",
            "page_count": 304,
            "language": "Türkçe",
            "rating": 8.4,
            "categories": ["Roman", "Macera", "Drama"],
        },
        {
            "title": "Ikigai",
            "author": "Francesc Miralles",
            "description": "Uluslararası çoksatan bir rehber olan Ikigai'yle her gününüz bir anlam kazansın. Japonlar herkesin bir ikigaisi olduğuna inanır, her sabah yataktan kalkmaları için bir sebepleri vardır. İlham verici ve rahatlatıcı bu kitap sizlere kendi ikigainizi keşfetmeniz için gerekli tüm bilgileri veriyor. Aceleci davranmamanızı, hayat gayenizi keşfetmenizi, ilişkilerinizi canlandırmanızı ve kendinizi tutkularınıza adamanızı sağlıyor.",
            "page_count": 176,
            "language": "Türkçe",
            "rating": 7.6,
            "categories": ["Kişisel Gelişim"],
        },
        {
            "title": "Beden Dili",
            "author": "Joe Navarro",
            "description": "İnsanları 'okuma'nın en hızlı yöntemi bu kitapta...Karşınızdakinin bedenine bakarak aklından geçenleri okumanız mümkün. Duygu ve düşünceleri çözümlemek, insanları doğru tanımak, tuzağa düşmemek, yalanı ortaya çıkarmak için beden dilini bilmeniz yeterli. Ayrıca beden dilinizi kullanarak patronunuz, aileniz, arkadaşlarınız ve diğer insanların sizinle ilgili düşüncelerini de değiştirebilirsiniz. Gerçek hisler yüzde gizlidir. Başparmaklar, ayaklar ve gözbebekleri ruh halimizi ortaya koyar. Kendimize duyduğumuz güveni konuşmalarımızdan önce bedenimiz yansıtır.",
            "page_count": 300,
            "language": "Türkçe",
            "rating": 8.2,
            "categories": ["Kişisel Gelişim", "Eğitim"],
        },
    ]
    
    # Default kapak resmi için basit bir içerik oluştur
    dummy_image = ContentFile(b'dummy-image', name='dummy-book-cover.jpg')
    
    for book_data in books_data:
        # Kategorileri bul
        book_categories = []
        for cat_name in book_data["categories"]:
            try:
                category = Category.objects.get(name=cat_name)
                book_categories.append(category)
            except Category.DoesNotExist:
                print(f"Kategori bulunamadı: {cat_name}")
        
        # Kitabı oluştur
        book, created = Book.objects.get_or_create(
            title=book_data["title"],
            defaults={
                "author": book_data["author"],
                "description": book_data["description"],
                "page_count": book_data["page_count"],
                "language": book_data["language"],
                "rating": book_data["rating"],
                "cover_image": dummy_image,
            }
        )
        
        if created:
            # Kategorileri ekle
            for category in book_categories:
                book.categories.add(category)
            print(f"Kitap oluşturuldu: {book.title}")
        else:
            print(f"Kitap zaten vardı: {book.title}")

if __name__ == "__main__":
    print("Örnek kategoriler ve kitaplar ekleniyor...")
    categories = add_categories()
    add_books(categories)
    print("İşlem tamamlandı!") 