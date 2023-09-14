// Выпадающее меню для Applications
document.addEventListener('DOMContentLoaded', function() {
    $('#table_applications').on('click', '.current-status', function() {
        var dropdownMenu = $(this).siblings('.dropdown-menu');
        
        // Закрываем предыдущее активное меню, если оно существует
        $('.dropdown-menu.show').not(dropdownMenu).hide();

        // Отображаем/скрываем текущее меню
        if (dropdownMenu.css('display') === 'none') {
            dropdownMenu.show();
        } else {
            dropdownMenu.hide();
        }
    });

    $('#table_applications').on('click', '.status-option', function() {
        var newStatus = $(this).text();
        var rowData = $('#table_applications').DataTable().row($(this).closest('tr')).data();
        var pk = rowData.num; // Замените это на ваш способ получения первичного ключа записи
        var clickedStatusOption = $(this); // Сохраняем ссылку на $(this) здесь
        var csrfToken = $('[name=csrfmiddlewaretoken]').val();

        $.ajax({
            type: 'POST',
            url: `/applications/updstatus/${pk}/`, // Замените это на URL для обновления статуса
            data: {
                status: newStatus,
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response) {
                // Обновляем отображение статуса
                rowData.status = newStatus;
                $('#table_applications').DataTable().row(clickedStatusOption.closest('tr')).data(rowData).draw();

                // Закрываем выпадающее меню
                clickedStatusOption.closest('.dropdown-menu').hide();
            },
            error: function() {
                alert('Ошибка при обновлении статуса.');
            }
        });
    });
});