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
        .then(response => {
            if (!response.ok) {
                throw new Error('Произошла ошибка при выполнении запроса');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // После успешного удаления, обновляем таблицу данных
                var table = $('#table_acts').DataTable();
                table.ajax.reload(null, false); // Этот метод обновит таблицу без перерисовки страницы
            } else {
                alert(data.message); // Выводим сообщение об ошибке
            }
        })
        .catch(error => {
            alert('Произошла ошибка: ' + error.message); // Выводим сообщение об ошибке
        });
    }
}


// Выпадающее меню
document.addEventListener('DOMContentLoaded', function() {
    // Получаем список всех кнопок с меню
    var dropdownButtons = document.querySelectorAll('.intable_dropdown_menu .dropdown_menu_button');
    var activeMenu = null; // Хранит активное меню

    // Добавляем обработчик событий к каждой кнопке
    $('#table_acts').on('click', '.dropdown_menu_button', function() {
        var buttonId = this.id;
        var menuId = buttonId.replace('dropdown_btn_', 'dropdown_menu_');
        var dropdownMenu = document.getElementById(menuId);
    
        // Закрываем предыдущее активное меню, если оно существует и не равно текущему меню
        var activeMenu = document.querySelector('.dropdown-menu.show');
        if (activeMenu && activeMenu !== dropdownMenu) {
            activeMenu.style.display = 'none';
        }
    
        // Отображаем/скрываем текущее меню
        if (dropdownMenu.style.display === 'none') {
            dropdownMenu.style.display = 'block';
        } else {
            dropdownMenu.style.display = 'none';
        }
    });

    // Обработчик изменения значения в поле "Оборудование"
    $('#id_inv_dit').on('select2:select', function (e) {
        console.log('Change event triggered.');
        var selectedValue = e.params.data.id;
        console.log('Selected value:', selectedValue)
        // Отправка асинхронного запроса на сервер для получения данных актов
        $.ajax({
            url: '/acts/get_acts/',  // URL-адрес, который будет обрабатывать запрос на сервере
            type: 'GET',
            data: {
                inv_dit: selectedValue
            },
            success: function (response) {
                // Очистка списка актов
                $('#acts-list').empty();

                // Обновление списка актов с данными из ответа сервера
                $.each(response.acts, function (index, act) {
                    var listItem = $('<li>');
                if (act.status === 'True') {
                    listItem.append($('<div>').addClass('act-date green').text(act.act_date));
                    listItem.append($('<div>').addClass('act-avtor green').text(act.avtor));
                    listItem.append($('<div>').addClass('act-result').text(act.result));
                    listItem.append($('<div>').addClass('act-conclusion').text(act.conclusion));
                    listItem.append($('<div>').addClass('act-type green').text(act.type));
                } else {
                    listItem.append($('<div>').addClass('act-date').text(act.act_date));
                    listItem.append($('<div>').addClass('act-avtor').text(act.avtor));
                    listItem.append($('<div>').addClass('act-result').text(act.result));
                    listItem.append($('<div>').addClass('act-conclusion').text(act.conclusion));
                    listItem.append($('<div>').addClass('act-type').text(act.type));
                }

                    $('#acts-list').append(listItem);
                });
            }
        });
    });
});

// Обработчик изменения значения в поле "Группы ОС" в acts/add_os/
document.addEventListener("DOMContentLoaded", function () {
    var osGroupField = document.getElementById("id_os_group"); // Получаем контейнер с выбранным значением
    var modelFields = document.getElementById("model-fields");
    var processorFields = document.getElementById("processor-fields");
    var ramFields = document.getElementById("ram-fields");
    var storageFields = document.getElementById("storage-fields");

    $('#id_os_group').on('select2:select', function (e) {
        console.log('Change event triggered.');
        var selectedValue = e.params.data.text;
        console.log('Selected value:', selectedValue)
        // Отправка асинхронного запроса на сервер для получения данных актов
        $.ajax({
            url: '/acts/add_os/',  // URL-адрес, который будет обрабатывать запрос на сервере
            type: 'GET',
            data: {
                os_group: selectedValue
            },
            success: function (response) {
                if (selectedValue === "Мини ПК" || selectedValue === "Ноутбук" || selectedValue === "Моноблок") {
                  modelFields.style.display = "block";
                  processorFields.style.display = "block";
                  ramFields.style.display = "block";
                  storageFields.style.display = "block";
                } else if (selectedValue === "Системный блок") {
                  modelFields.style.display = "none";
                  processorFields.style.display = "block";
                  ramFields.style.display = "block";
                  storageFields.style.display = "block";
                } else {
                  modelFields.style.display = "block";
                  processorFields.style.display = "none";
                  ramFields.style.display = "none";
                  storageFields.style.display = "none";
                }
            }
        });
    });
});

function updateStatusOnActs(pk, newStatus) {
    var csrfToken = $('[name=csrfmiddlewaretoken]').val();

    $.ajax({
        type: 'POST',
        url: `/acts/updstatus/${pk}/`,
        data: {
            status: newStatus,
            csrfmiddlewaretoken: csrfToken
        },
        success: function(response) {
            // Обновляем отображение статуса
            var table = $('#table_acts').DataTable();
            var rowData = table.row($(`#dropdown_btn_${pk}`).closest('tr')).data();
            rowData.status = newStatus;
            table.row($(`#dropdown_btn_${pk}`).closest('tr')).data(rowData).draw();

            // Закрываем выпадающее меню
            $(`#dropdown_menu_${pk}`).hide();

            // Перерисовываем таблицу
            table.ajax.reload();
        },
        error: function() {
            alert('Ошибка при обновлении статуса.');
        }
    });
}
