function confirmDelete(url, actsUrl) {
    if (confirm('Вы уверены, что хотите удалить эту запись?')) {
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken') // Получение значения токена CSRF из куки
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Дополнительная обработка успешного удаления или ошибки
            if (data.message) {
                // Успешное удаление, обновляем список актов
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
                        // Обработка ошибки обновления списка
                    });
            } else {
                // Обработка других сообщений или ошибок
            }
        })
        .catch(error => {
            console.error('Произошла ошибка:', error);
            // Обработка ошибки
        });
    }
}
