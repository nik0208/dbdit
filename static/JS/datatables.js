$(document).ready(function() {
    function initializeDataTable(tableId, ajaxUrl, columns) {
        var table = $(tableId).DataTable({
            "processing": true,
            "serverSide": true,
            "ajax": ajaxUrl,
            "columns": columns,
            "dom": '<"top"i>rt<"bottom"flp><"clear">',
            "language": {
                "info": "Показано _START_ - _END_ из _TOTAL_ записей",
                "lengthMenu": "Показать _MENU_ записей на странице",
                "search": "Поиск:",
                "paginate": {
                    "first": "<<",
                    "last": ">>",
                    "next": ">",
                    "previous": "<"
                }
            },
            "pageLength": 50,
            "initComplete": function(settings, json) {
                $('.bottom .dataTables_paginate').appendTo('#table-pagination');
                $('.dataTables_paginate').addClass('step-links');
                $('.dataTables_paginate').find('a').addClass('page-link');
                $('.dataTables_paginate').find('.current').addClass('current-page');
            }
        });

        $('#customSearchBox').on('keyup', function() {
            table.search(this.value).draw();
        });

        $('#table_os_length').on('change', function() {
            table.page.len($(this).val()).draw();
        });
    }

    initializeDataTable('#table_os', '/directories/os_list/', [
        { "data": "inv_dit" },
        { "data": "name_os" },
        { "data": "inpute_date" },
        { "data": "os_group" },
        { "data": "serial_number" },
        { "data": "original_price" }
    ]);

    initializeDataTable('#table_tmc', '/directories/tmc_list/', [
        { "data": "tmc_name" },
        { "data": "tmc_article" },
        { "data": "web_code" },
        { "data": "tmc_price" }
    ]);

    initializeDataTable('#table_moves', '/moves/moves_list/', [
        { "data": "move_type" },
        { "data": "move_num" },
        { "data": "move_date" },
        { "data": "user" },
        { "data": "sklad" },
        { "data": "comment" },
        { "data": "pk", render: function (data, type, row) {
            return '<a href="/moves/generatemovedocument/' + data + '">Создать</a>';
        }},
    ]);

    initializeDataTable('#table_acts', '/acts/acts_list/', [
        { "data": "pk" },
        { "data": "act_date" },
        { "data": "inv_dit" },
        { "data": "result" },
        { "data": "conclusion" },
        { "data": "user" },
        { "data": "sklad" },
        { "data": "type" },        
        { "data": "avtor" },
        {
            "data": "pk",
            "render": function(data, type, row) {
                // Верните содержимое ячейки в виде HTML-кода, включая ваш блок
                return `
                    <td>
                        <div class="intable_dropdown_menu">
                            <!-- Ваш блок здесь -->
                            <!-- Пример: -->
                            <button id="dropdown_btn_${row.pk}" class="dropdown_menu_button" data-dropdown-id="${row.pk}">
                                <img src="/static/icons/list.svg" alt="Действия" class="dropdown_menu_button_image">
                            </button>
                            <div id="dropdown_menu_${row.pk}" class="dropdown-menu" style="display: none;">
                                <ul>
                                    <li><a href="{% comment %} {% url 'act_edit' acts.id %} {% endcomment %}">Изменить</a></li>
                                    <li><a href="#" onclick="{% comment %} confirmDelete('{% url 'act_delete' acts.id %}', '{% url 'acts' %}') {% endcomment %}">Удалить</a></li>
                                    <li><a href="/acts/generate_act_document/${data}">Печать</a></li>
                                    <div id="dropdown_submenu_{{ acts.id }}" class="dropdown_submenu">
                                        <ul>
                                            <li class="submenu_title"><a href="#" class="submenu_title">Создать на основании</a></li>
                                            <li><a href="#">Перемещение</a></li>
                                            <li><a href="#">Комплектация</a></li>
                                            <li><a href="#">Перевод товаров</a></li>
                                        </ul>
                                    </div>
                                </ul>
                            </div>
                        </div>
                    </td>
                `;
            }
        }
    ]);

    initializeDataTable('#table_applications', '/applications/applications_list/', [
        { "data": "num" },
        { "data": "requested_equipment" },
        { "data": "avtor" },
        { "data": "user" },
        { "data": "date" },
        { "data": "deadline" },
        { "data": "department" },
        { "data": "status" },
    ]);

    initializeDataTable('#table_complectations', '/complectations/complectations_list/', [
        { "data": "pk" },
        { "data": "date" },
        { "data": "avtor" },
        { "data": "inv_dit" },
        { "data": "tmc" },
        { "data": "tmc_qty" },
        { "data": "par_doc" },
    ]);
});