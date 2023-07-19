$(document).ready(function() {
  $('.form-field.select').select2();
  $('.form-field.select.multi').select2({
    multiple: true,
  });
});
  
  // Получение ссылок на элементы форм
  document.addEventListener('DOMContentLoaded', function() {
    const toggleSwitch = document.getElementById('toggle');
    const osForm = document.getElementById('osForm');
    const tmcForm = document.getElementById('tmcForm');

    toggleSwitch.addEventListener('change', function() {
      if (toggleSwitch.checked) {
        osForm.style.display = 'none';
        tmcForm.style.display = 'block';
      } else {
        osForm.style.display = 'block';
        tmcForm.style.display = 'none';
      }
    });
  });

  $(document).ready(function() {
    $('#equipment').select2();
  });