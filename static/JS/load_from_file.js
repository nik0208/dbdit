function openFileUploadDialog() {
    var modal = document.getElementById("uploadModal");
    modal.style.display = "block";
}

function closeFileUploadDialog() {
    var modal = document.getElementById("uploadModal");
    modal.style.display = "none";
}

function uploadExcel() {
    var fileInput = document.getElementById('excel-file');
    var uploadUrl = fileInput.getAttribute('data-upload-url');
    
    fileInput.addEventListener('change', function() {
        // Rest of your code
        // Use the uploadUrl variable as the URL for your XMLHttpRequest
        var xhr = new XMLHttpRequest();
        xhr.open('POST', uploadUrl, true);
        // Rest of your code
    });
}

// Запускаем функцию uploadExcel при загрузке страницы
document.addEventListener("DOMContentLoaded", function() {
    uploadExcel();
});

document.addEventListener("DOMContentLoaded", function() {
    var loadFileLink = document.querySelector(".load_file");
    loadFileLink.addEventListener("click", openFileUploadDialog);
});






// Обработка перетаскивания
var dropZone = document.getElementById('drop_zone');
dropZone.addEventListener('dragover', function(e) {
    e.stopPropagation();
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
});

dropZone.addEventListener('drop', function(e) {
    e.stopPropagation();
    e.preventDefault();
    var files = e.dataTransfer.files; // Список файлов
    handleFiles(files);
});

// Логика обработки файла
function handleFiles(files) {
    var file = files[0];
    // Здесь вы можете отправить файл на сервер или обработать его на клиенте
    console.log(file);
}

var radioButtons = document.getElementsByName('optionGroup');
for(var i = 0; i < radioButtons.length; i++) {
    radioButtons[i].addEventListener('change', function() {
        if(this.checked) {
            // Радиокнопка выбрана
            console.log(this.value);
        }
    });
}
