document.addEventListener('DOMContentLoaded', function() {
    const accessToken = localStorage.getItem('access_token');
    const isSpecial = localStorage.getItem('is_special') === 'true';

    if (accessToken) {
        document.getElementById('profile-btn').style.display = 'inline-block';
        document.getElementById('logout-btn').style.display = 'inline-block';

        if (isSpecial) {
            document.getElementById('join-btn').style.display = 'inline-block'; 
        }
    }
});


document.getElementById('register-open-btn').addEventListener('click', function () {
    document.getElementById('register-form').style.display = 'block';
});

document.getElementById('login-open-btn').addEventListener('click', function () {
    document.getElementById('login-form').style.display = 'block';
});

document.querySelectorAll('.close-btn').forEach(btn => {
    btn.addEventListener('click', function () {
        this.parentElement.style.display = 'none';
    });
});


document.getElementById('register-btn').addEventListener('click', function () {
    const userData = {
        username: document.getElementById('register-username').value,
        email: document.getElementById('register-email').value,
        password: document.getElementById('register-password').value,
        phone: document.getElementById('register-phone').value,
        is_special: document.getElementById('register-is-special').value === "true"
    };

    fetch('http://127.0.0.1:8000/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert('Реєстрація успішна!');
            document.getElementById('register-form').style.display = 'none';
        } else {
            alert('Помилка: ' + JSON.stringify(data));
        }
    })
    .catch(error => console.error('Помилка:', error));
});


document.getElementById('login-btn').addEventListener('click', () => {
    const loginData = {
        username: document.getElementById('login-email').value,
        password: document.getElementById('login-password').value
    };

    fetch('http://127.0.0.1:8000/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(loginData),
    })
    .then(response => response.json())
    .then(data => {
        if (data.access) {
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            localStorage.setItem('is_special', data.is_special); 
            
            alert('Успішний вхід!');
            document.getElementById('login-form').style.display = 'none';
            document.getElementById('logout-btn').style.display = 'inline-block';
            document.getElementById('profile-btn').style.display = 'inline-block';

            if (data.is_special) {
                document.getElementById('join-btn').style.display = 'inline-block'; 
            }
        } else {
            alert('Помилка входу: ' + (data.message || 'Невірний логін або пароль'));
        }
    })
    .catch(error => console.error('Помилка:', error));
});




document.getElementById('logout-btn').addEventListener('click', function () {
    
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('is_special');
    location.reload();

    
    
});


document.getElementById('profile-btn').addEventListener('click', function() {
    window.location.href = 'profile.html';
});



document.addEventListener("DOMContentLoaded", function () {
    fetch("http://127.0.0.1:8000/posts/") 
        .then(response => response.json())
        .then(posts => {
            const postList = document.getElementById("post-list");
            posts.forEach(post => {
                const postItem = document.createElement("li");
                postItem.textContent = post.title;
                postItem.style.cursor = "pointer";
                postItem.addEventListener("click", function () {
                    window.location.href = `post.html?id=${post.id}`;
                });
                postList.appendChild(postItem);
            });
        })
        .catch(error => console.error("Помилка при отриманні постів:", error));
});


document.getElementById('join-btn').addEventListener('click', function() {
    alert('Ви долучилися як спеціальний користувач!');
});