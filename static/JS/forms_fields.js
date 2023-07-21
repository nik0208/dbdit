$(document).ready(function() {
  $('.form-field.select').select2();
});
  
// document.addEventListener("DOMContentLoaded", function() {
//   const toggleSwitch = document.getElementById("toggle");
//   const osForm = document.getElementById("osForm");
//   const tmcForm = document.getElementById("tmcForm");
//   const selectedEquipmentOs = document.getElementById("selected_equipment_os");
//   const selectedEquipmentTmc = document.getElementById("selected_equipment_tmc");

//   toggleSwitch.addEventListener("change", function() {
//     if (toggleSwitch.checked) {
//       osForm.style.display = "none";
//       tmcForm.style.display = "flex";
//       selectedEquipmentOs.style.display = "none";
//       selectedEquipmentTmc.style.display = "block";
//     } else {
//       osForm.style.display = "flex";
//       tmcForm.style.display = "none";
//       selectedEquipmentOs.style.display = "block";
//       selectedEquipmentTmc.style.display = "none";
//     }
//   });
// });