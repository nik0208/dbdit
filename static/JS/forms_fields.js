$(document).ready(function() {
  $('.form_field.select').select2();
  $('.form_field.select.multi').select2({
      multiple: true,
  });
});

$(document).ready(function() {
    function initializeSelect2Ajax(selector, url) {
      $(selector).select2({
        minimumInputLength: 2,
        ajax: {
          url: url,
          dataType: 'json',
          delay: 250,
          processResults: function(data) {
            return {
              results: data
            };
          },
          cache: true
        }
      });
    }
  
    var equipmentUrl = $('.js-url-field').data('url');
    initializeSelect2Ajax('#id_equipment', equipmentUrl);
    // Добавьте вызовы initializeSelect2Ajax для других полей, если необходимо
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
