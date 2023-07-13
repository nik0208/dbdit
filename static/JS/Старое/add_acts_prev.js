$(document).ready(function () {
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
          listItem.append($('<div>').addClass('act-date').text(act.act_date));
          listItem.append($('<div>').addClass('act-avtor').text(act.avtor));
          listItem.append($('<div>').addClass('act-result').text(act.result));
          listItem.append($('<div>').addClass('act-conclusion').text(act.conclusion));
          listItem.append($('<div>').addClass('act-type').text(act.type));
          $('#acts-list').append(listItem);
        });
      }
    });
  });
});
