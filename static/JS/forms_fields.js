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

  document.addEventListener("DOMContentLoaded", function() {
    const equipmentSelect = document.getElementById("id_equipment_tmc");
    equipmentSelect.addEventListener("change", updateSelectedEquipment);
  
    function updateSelectedEquipment() {
      const selectedEquipmentTable = document.getElementById("selected-equipment-table");
      const selectedEquipmentBody = selectedEquipmentTable.getElementsByTagName("tbody")[0];
      selectedEquipmentBody.innerHTML = ""; // Очистить предыдущие данные
  
      const selectedOptions = Array.from(equipmentSelect.selectedOptions);
  
      selectedOptions.forEach(function(option) {
        const equipmentId = option.value;
        const row = document.createElement("tr");
  
        // Создание ячеек для каждого столбца
        const nameCell = document.createElement("td");
        const userCell = document.createElement("td");
        const skladCell = document.createElement("td");
        const costCell = document.createElement("td");
  
        // Установка сообщения о загрузке в ячейки
        nameCell.textContent = option.text;
        userCell.textContent = "Загрузка...";
        skladCell.textContent = "Загрузка...";
        costCell.textContent = "Загрузка...";
  
        row.appendChild(nameCell);
        row.appendChild(userCell);
        row.appendChild(skladCell);
        row.appendChild(costCell);
  
        selectedEquipmentBody.appendChild(row);
  
        // Асинхронное получение дополнительных данных
        fetch('/get_additional_data/' + equipmentId)
          .then(response => response.json())
          .then(data => {
            // Обновление значений ячеек полученными данными
            userCell.textContent = data.user;
            skladCell.textContent = data.sklad;
            costCell.textContent = data.cost;
          })
          .catch(error => {
            console.error('Ошибка:', error);
          });
      });
    }
  
    updateSelectedEquipment();
  });
  