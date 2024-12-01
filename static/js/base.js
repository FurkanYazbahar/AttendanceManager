document.addEventListener("DOMContentLoaded", function () {
    const authControls = document.getElementById('navbar-auth');
    const roleBasedMenu = document.getElementById('role-based-menu');

    // authControls ve roleBasedMenu'nun DOM'da bulunup bulunmadığını kontrol edin
    if (!authControls) {
        console.error('authControls bulunamadı.');
        return;
    }
    if (!roleBasedMenu) {
        console.error('roleBasedMenu bulunamadı.');
        return;
    }

    const token = localStorage.getItem('access_token');
    const user_role = localStorage.getItem('user_role');
    const username = localStorage.getItem('username');

    // Token ve kullanıcı bilgileri kontrolü
    if (token && user_role && username) {
        // Rol tabanlı menü oluşturma
        if (user_role === 'admin') {
            roleBasedMenu.innerHTML = `
                <li class="nav-item">
                    <a class="nav-link" href="/admin/dashboard/">Yönetici Paneli</a>
                </li>
            `;
        } else if (user_role === 'user') {
            roleBasedMenu.innerHTML = `
                <li class="nav-item">
                    <a class="nav-link" href="/user/profile/">Profilim</a>
                </li>
            `;
        } else {
            console.warn('Geçersiz kullanıcı rolü:', user_role);
        }

        // Kullanıcı menüsü
        authControls.innerHTML = `
            <li class="nav-item">
                <span class="nav-link">Merhaba, ${username}</span>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#" id="logout">Çıkış Yap</a>
            </li>
        `;

        // Çıkış işlemi
        document.getElementById('logout').addEventListener('click', async function () {
            try {
                // Backend'e çıkış isteği gönder
                const response = await fetch('/api/logout/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                });

                if (response.ok) {
                    // Başarılıysa, localStorage'u temizle ve yönlendirme yap
                    localStorage.clear();
                    window.location.href = '/login/';
                } else {
                    console.error('Logout işlemi başarısız:', await response.json());
                }
            } catch (error) {
                console.error('Logout sırasında hata:', error);
            }
        });
    } else {
        // Giriş yapılmadıysa
        console.warn('Giriş yapılmadı veya eksik kullanıcı bilgisi.');
        authControls.innerHTML = `
            <li class="nav-item">
                <a class="nav-link" href="/login/">Giriş Yap</a>
            </li>
        `;
    }
});
document.addEventListener("DOMContentLoaded", function () {
    const currentPath = window.location.pathname;
    const menuItems = document.querySelectorAll('.nav-link');

    menuItems.forEach(item => {
        if (item.getAttribute('href') === currentPath) {
            item.classList.add('active');
        }
    });
});
