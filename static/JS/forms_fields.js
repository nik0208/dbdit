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
  