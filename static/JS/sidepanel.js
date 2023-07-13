$(document).ready(function() {
  // Получение значения состояния боковой панели из локального хранилища
  var sidebarState = localStorage.getItem('sidebarState');
  if (sidebarState === 'closed') {
    // Если состояние боковой панели было сохранено как закрытое, добавляем классы "sidebar-closed" к соответствующим элементам
    $(".toggle").addClass("sidebar-closed");
    $(".sidebar").addClass("sidebar-closed");
    $(".contentpanel").addClass("sidebar-closed");
    $(".LoggedUserName").addClass("sidebar-closed");
  }

  $("#toggle-sidebar-btn").click(function() {
    $(".toggle").toggleClass("sidebar-closed");
    $(".sidebar").toggleClass("sidebar-closed");
    $(".contentpanel").toggleClass("sidebar-closed");
    $(".LoggedUserName").toggleClass("sidebar-closed");

    // Сохранение состояния боковой панели в локальное хранилище
    if ($(".toggle").hasClass("sidebar-closed")) {
      localStorage.setItem('sidebarState', 'closed');
    } else {
      localStorage.setItem('sidebarState', 'open');
    }
  });
});