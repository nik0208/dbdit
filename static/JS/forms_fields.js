$(document).ready(function() {
  $('.form-field.select').select2({
    minimumInputLength: 3,
  });
  $('.form-field.select.multi').select2({
    multiple: true,
    minimumInputLength: 3,
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
        tmcForm.style.display = 'flex';
      } else {
        osForm.style.display = 'flex';
        tmcForm.style.display = 'none';
      }
    });
  });