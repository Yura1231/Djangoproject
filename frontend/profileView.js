document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', function () {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            const tabId = this.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });

    
    
});



document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get('userId'); // Отримуємо userId з URL
    const accessToken = localStorage.getItem("access_token"); 

    if (!accessToken) {
        alert("Будь ласка, увійдіть у свій акаунт.");
        window.location.href = "login.html"; 
        return;
    }

    if (!userId) {
        // Якщо userId не передано в URL, перенаправляємо на головну
        window.location.href = 'index.html';
        return;
    }

    
    fetch(`http://127.0.0.1:8000/profile/${userId}/`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${accessToken}`,
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Помилка отримання профілю");
        }
        return response.json();
    })
    .then(data => {
        document.getElementById("userName").textContent = `${data.first_name} ${data.last_name}`;
        

        if (data.profile_picture) {
            document.getElementById("profilePhoto").src = `http://127.0.0.1:8000${data.profile_picture}`;
        }

        if (data.description) {
            document.getElementById("content").value = data.description;
        }
    })
    .catch(error => {
        console.error("Помилка:", error);
    });
        

        

        
            
        

    
});



document.addEventListener("DOMContentLoaded", async () => {
    const publishBtn = document.getElementById("publishBtn");
    const commentInput = document.getElementById("comment");
    const reviewsContainer = document.getElementById("reviews");
    if (!commentInput) {
        console.error("Помилка: Поле коментаря не знайдено в DOM!");
        return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get("userId"); // Переконайтеся, що параметр в URL саме "userId"
    console.log("userId:", userId);  // Отримуємо ID користувача з URL
    const accessToken = localStorage.getItem("access_token"); 

    // Функція отримання відгуків
    async function fetchReviews() {
        try {
            let response = await fetch(`http://127.0.0.1:8000/comments/${userId}/`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Content-Type": "application/json"
                }
            });

            if (!response.ok) throw new Error("Не вдалося завантажити відгуки");

            let comments = await response.json();

            reviewsContainer.innerHTML = ""; // Очищуємо контейнер перед додаванням

            if (comments.length === 0) {
                reviewsContainer.innerHTML = `<div class="content-box default-text">Відгуки про користувача відсутні.</div>`;
                return;
            }

            comments.forEach(comment => {
                const commentElement = document.createElement("div");
                commentElement.classList.add("content-box");
            
                commentElement.innerHTML = `
                    <div class="review-item">
                        <img src="http://127.0.0.1:8000${comment.author_profile_picture}" alt="User Avatar" class="user-avatar">
                        <div class="review-content">
                            <span class="user-name">${comment.author_first_name}  ${comment.author_last_name}</span>
                            <p class="review-text">${comment.text}</p>
                            <small>${new Date(comment.created_at).toLocaleString()}</small>
                        </div>
                    </div>
                `;
            
                reviewsContainer.appendChild(commentElement);
            });

        } catch (error) {
            console.error("Помилка:", error);
            reviewsContainer.innerHTML = `<div class="content-box default-text">Не вдалося завантажити відгуки.</div>`;
        }
    }

    // Функція надсилання відгуку
    publishBtn.addEventListener("click", async () => {
        const text = commentInput.value.trim();
        if (!text) return alert("Коментар не може бути порожнім!");

        try {
            let response = await fetch(`http://127.0.0.1:8000/comments/${userId}/`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text })
            });

            if (!response.ok) throw new Error("Не вдалося залишити коментар");

            commentInput.value = ""; // Очищуємо поле
            fetchReviews(); // Оновлюємо список відгуків

        } catch (error) {
            console.error("Помилка:", error);
            alert("Не вдалося залишити коментар.");
        }
    });

    fetchReviews(); // Завантажуємо відгуки при завантаженні сторінки
});
