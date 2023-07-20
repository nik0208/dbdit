$(document).ready(function() {
  $('.form-field.select').select2({
    minimumInputLength: 3,
  });
  $('.form-field.select.multi').select2({
    multiple: true,
    minimumInputLength: 3,
  });
});
  
document.addEventListener("DOMContentLoaded", function() {
  const toggleSwitch = document.getElementById("toggle");
  const osForm = document.getElementById("osForm");
  const tmcForm = document.getElementById("tmcForm");
  const selectedEquipmentOs = document.getElementById("selected_equipment_os");
  const selectedEquipmentTmc = document.getElementById("selected_equipment_tmc");

  toggleSwitch.addEventListener("change", function() {
    if (toggleSwitch.checked) {
      osForm.style.display = "none";
      tmcForm.style.display = "flex";
      selectedEquipmentOs.style.display = "none";
      selectedEquipmentTmc.style.display = "block";
    } else {
      osForm.style.display = "flex";
      tmcForm.style.display = "none";
      selectedEquipmentOs.style.display = "block";
      selectedEquipmentTmc.style.display = "none";
    }
  });

  const equipmentSelectOs = document.getElementById("id_equipment_os");
  const equipmentSelectTmc = document.getElementById("id_equipment_tmc");

  equipmentSelectOs.addEventListener("change", updateSelectedEquipmentOs);
  equipmentSelectTmc.addEventListener("change", updateSelectedEquipmentTmc);

  function updateSelectedEquipmentOs() {
    const selectedEquipmentTable = document.getElementById("selected-equipment-table-os");
    const selectedEquipmentBody = selectedEquipmentTable.getElementsByTagName("tbody")[0];

    selectedEquipmentBody.innerHTML = "";

    const selectedOptions = Array.from(equipmentSelectOs.selectedOptions);

    selectedOptions.forEach(function(option) {
      const name = option.text;
      const description = option.dataset.description;

      const row = document.createElement("tr");
      const nameCell = document.createElement("td");
      const descriptionCell = document.createElement("td");

      nameCell.textContent = name;
      descriptionCell.textContent = description;

      row.appendChild(nameCell);
      row.appendChild(descriptionCell);

      selectedEquipmentBody.appendChild(row);
    });
  }

  updateSelectedEquipmentOs();


  function updateSelectedEquipmentTmc() {
    const selectedEquipmentTable = document.getElementById("selected-equipment-table-tmc");
    const selectedEquipmentBody = selectedEquipmentTable.getElementsByTagName("tbody")[0];

    selectedEquipmentBody.innerHTML = "";

    const selectedOptions = Array.from(equipmentSelectTmc.selectedOptions);

    selectedOptions.forEach(function(option) {
      const name = option.text;
      const description = option.dataset.description;

      const row = document.createElement("tr");
      const nameCell = document.createElement("td");
      const descriptionCell = document.createElement("td");

      nameCell.textContent = name;
      descriptionCell.textContent = description;

      row.appendChild(nameCell);
      row.appendChild(descriptionCell);

      selectedEquipmentBody.appendChild(row);
    });
  }

  updateSelectedEquipmentOs();
  updateSelectedEquipmentTmc();
});