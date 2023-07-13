// act_delete.js

// Функция для получения значения токена CSRF из куки
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Функция для подтверждения удаления акта
function confirmDelete(url, actsUrl) {
    if (confirm('Вы уверены, что хотите удалить эту запись?')) {
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.message) {
                fetch(actsUrl)
                    .then(response => response.text())
                    .then(html => {
                        const parser = new DOMParser();
                        const newDocument = parser.parseFromString(html, 'text/html');
                        const newContent = newDocument.querySelector('.contentpanel');
                        const oldContent = document.querySelector('.contentpanel');
                        oldContent.innerHTML = newContent.innerHTML;
                    })
                    .catch(error => {
                        console.error('Ошибка при обновлении списка:', error);
                    });
            } else {
                // Обработка других сообщений или ошибок
            }
        })
        .catch(error => {
            console.error('Произошла ошибка:', error);
        });
    }
}
