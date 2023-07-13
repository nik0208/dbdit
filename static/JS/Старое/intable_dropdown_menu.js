document.addEventListener('DOMContentLoaded', function() {
    // Получаем список всех кнопок с меню
    var dropdownButtons = document.querySelectorAll('.intable_dropdown_menu .dropdown_menu_button');
    var activeMenu = null; // Хранит активное меню

    // Добавляем обработчик событий к каждой кнопке
    dropdownButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var buttonId = this.id;
            var menuId = buttonId.replace('dropdown_btn_', 'dropdown_menu_');
            var dropdownMenu = document.getElementById(menuId);

            // Закрываем предыдущее активное меню, если оно существует и не равно текущему меню
            if (activeMenu && activeMenu !== dropdownMenu) {
                activeMenu.style.display = 'none';
            }

            if (dropdownMenu.style.display === 'none') {
                dropdownMenu.style.display = 'block';
                activeMenu = dropdownMenu; // Обновляем активное меню
            } else {
                dropdownMenu.style.display = 'none';
                activeMenu = null; // Сбрасываем активное меню
            }
        });
    });
});

