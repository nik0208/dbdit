document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('fileInput');

    fileInput.addEventListener('change', function (event) {
        const file = event.target.files[0]; // Получаем выбранный файл

        if (!file) {
            return; // Если файл не выбран, ничего не делаем
        }

        // Проверка типа файла
        const fileExtension = file.name.split('.').pop().toLowerCase();
        if (fileExtension !== 'csv' && fileExtension !== 'xlsx') {
            alert('Неверный тип файла. Пожалуйста, загрузите CSV или Excel файл.');
            return;
        }

        // Далее вы можете использовать FileReader для чтения или другой обработки файла
        const reader = new FileReader();
        reader.onload = function (e) {
            const contents = e.target.result;
            // Теперь переменная `contents` содержит содержимое файла. Вы можете его обработать здесь.
        };
        reader.readAsText(file); // Читаем содержимое файла
    });
});
