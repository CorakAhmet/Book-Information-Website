// Tema değişimini yöneten JavaScript 

// Sayfa yüklendiğinde
document.addEventListener('DOMContentLoaded', function() {
    const themeSwitch = document.getElementById('themeSwitch');
    
    // Arayüzde tema geçişi için event listener ekleme
    if (themeSwitch) {
        themeSwitch.addEventListener('change', function() {
            const newTheme = this.checked ? 'dark' : 'light';
            applyTheme(newTheme);
            
            // Formu gönderme - tema değişikliğini kaydetme 
            // (Form içindeki onchange event'i ile zaten yapılıyor, ama ek önlem)
            if (this.form) {
                this.form.submit();
            }
        });
    }
    
    // Tarayıcı sistem tercihi değiştiğinde otomatik tema değişimi (opsiyonel)
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    prefersDarkScheme.addEventListener('change', (e) => {
        // Kullanıcı tarayıcı/sistem ayarlarını değiştirdiyse
        // NOT: Kullanıcı sitede manuel tema seçtiyse bu özelliği kullanmak istemeyebilirsiniz
        // Bu durumda bu kısmı yoruma alabilir ya da kaldırabilirsiniz
        /*
        const newTheme = e.matches ? 'dark' : 'light';
        applyTheme(newTheme);
        */
    });
    
    // Temayı başlangıçta kontrol et ve uygula
    const storedTheme = localStorage.getItem('theme');
    if (storedTheme) {
        applyTheme(storedTheme);
    }
});

// Mevcut temayı al
function getCurrentTheme() {
    // Önce localStorage'dan kontrol et
    const storedTheme = localStorage.getItem('theme');
    if (storedTheme) {
        return storedTheme;
    }
    
    // Sonra HTML data-theme özelliğinden temayı al
    const htmlElement = document.documentElement;
    return htmlElement.getAttribute('data-theme') || 'light';
}

// Temayı uygula
function applyTheme(theme) {
    const htmlElement = document.documentElement;
    htmlElement.setAttribute('data-theme', theme);
    
    // localStorage'a temayı kaydet
    localStorage.setItem('theme', theme);
    
    // Tema ayarlarını güncelle
    updateThemeElements(theme);
}

// Tema değişince güncellenmesi gereken elementleri güncelle
function updateThemeElements(theme) {
    const themeSwitch = document.getElementById('themeSwitch');
    
    // Switch'in durumunu güncelle
    if (themeSwitch) {
        themeSwitch.checked = theme === 'dark';
        
        // Label içindeki ikonu güncelle
        const label = themeSwitch.nextElementSibling;
        if (label && label.tagName === 'LABEL') {
            const icon = label.querySelector('i');
            if (icon) {
                if (theme === 'dark') {
                    icon.className = 'fas fa-moon';
                } else {
                    icon.className = 'fas fa-sun';
                }
            }
        }
    }
}

// Tema geçişi - ana fonksiyon
function toggleTheme() {
    // Mevcut temayı al
    const currentTheme = getCurrentTheme();
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    // Temayı görsel olarak uygula
    applyTheme(newTheme);
    
    // Tema değişikliğini sunucuya kaydet
    saveTemePreference(newTheme);
    
    // Buton metnini güncelle
    updateThemeButton(newTheme);
}

// Tema tercihini sunucuya kaydet
function saveTemePreference(theme) {
    const csrfToken = document.getElementById('csrf_token').value;
    
    fetch('/accounts/theme-switch/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: `theme=${theme}`
    })
    .then(response => {
        if (!response.ok) {
            console.error('Tema değişikliği kaydedilemedi');
        }
    })
    .catch(error => {
        console.error('Tema değişikliği kaydedilirken hata:', error);
    });
}

// Tema butonunu güncelle
function updateThemeButton(theme) {
    const themeButton = document.querySelector('button[onclick="toggleTheme()"]');
    if (!themeButton) return;
    
    if (theme === 'dark') {
        themeButton.innerHTML = '<i class="fas fa-sun"></i> Açık Mod';
        themeButton.classList.remove('btn-dark');
        themeButton.classList.add('btn-light');
    } else {
        themeButton.innerHTML = '<i class="fas fa-moon"></i> Karanlık Mod';
        themeButton.classList.remove('btn-light');
        themeButton.classList.add('btn-dark');
    }
} 