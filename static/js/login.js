document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.slide-button button');
    const forms = {
        personel: document.getElementById('personelForm'),
        yetkili: document.getElementById('yetkiliForm')
    };

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            buttons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            button.classList.add('active');

            // Hide all forms
            Object.values(forms).forEach(form => form.classList.remove('active'));
            // Show selected form
            const targetForm = button.getAttribute('data-target');
            forms[targetForm].classList.add('active');
        });
    });

    // Form submission handling
    forms.personel.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = forms.personel.querySelector('input[type="text"]').value;
        const password = forms.personel.querySelector('input[type="password"]').value;

        try {
            const data = await login(username, password);
            const accessToken = data.access;
            const refreshToken = data.refresh;

            // Token'ları localStorage'e kaydet
            localStorage.setItem('access_token', accessToken);
            localStorage.setItem('refresh_token', refreshToken);            

            // Role dayalı yönlendirme
            const user = await user_info(data.access);
            localStorage.setItem('user_role', user.role);
            localStorage.setItem('username', user.username);
            localStorage.setItem('user_id', user.user_id);
            navigateBasedOnRole(user.role);
            
        } catch (error) {
            alert("Personel girişi başarısız: " + error.message);
        }
    });

    forms.yetkili.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = forms.yetkili.querySelector('input[type="text"]').value;
        const password = forms.yetkili.querySelector('input[type="password"]').value;

        try {
            const data = await login(username, password);
            const accessToken = data.access;
            const refreshToken = data.refresh;

            // Token'ları localStorage'e kaydet
            localStorage.setItem('access_token', accessToken);
            localStorage.setItem('refresh_token', refreshToken);            

            // Role dayalı yönlendirme
            const user = await user_info(data.access);
            localStorage.setItem('user_role', user.role);
            localStorage.setItem('username', user.username);
            localStorage.setItem('user_id', user.user_id);
            navigateBasedOnRole(user.role);
            
        } catch (error) {
            alert("Yetkili girişi başarısız: " + error.message);
        }
    });
});

async function login(username, password) {
    const response = await fetch("http://localhost:8000/api/token/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
        const data = await response.json();
        return data;

    } else {
        const errorData = await response.json();        
        throw new Error(errorData.message || "Login failed");
    }
}
async function user_info(token) {
    // Kullanıcı rolünü almak için /api/user/ endpoint'ine istek
    const response = await fetch('/api/user/', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
            }
    });

    if (!response.ok) {
        throw new Error('Kullanıcı bilgileri alınamadı.');
    }

    return await response.json();
}

function navigateBasedOnRole(role) {
    if (role === "admin") {
        window.location.href = "/admin/dashboard/";
    } else if (role === "user") {
        window.location.href = "/user/profile/";
    } else {
        alert('Geçersiz rol: ' + role);
    }
}
