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

