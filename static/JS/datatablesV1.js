$(document).ready(function () {
    function initializeDataTable(tableId, ajaxUrl, columns, defaultSort) {
        var table = $(tableId).DataTable({
            "processing": true,
            "serverSide": true,
            "ajax": ajaxUrl,
            "columns": columns,
            "order": defaultSort, // Устанавливаем сортировку по умолчанию
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
            "initComplete": function (settings, json) {
                $('.bottom .dataTables_paginate').appendTo('#table-pagination');
                $('.dataTables_paginate').addClass('step-links');
                $('.dataTables_paginate').find('a').addClass('page-link');
                $('.dataTables_paginate').find('.current').addClass('current-page');
            },

            //Цветовая индикация таблиц START

            "createdRow": function (row, data, dataIndex) {
                if (data.status === 'True' || data.status === 'Завершена' || data.status === 'Отклонена') {
                    // Если статус True или Завершена, добавьте класс green-row
                    $(row).addClass('green-row');
                }
                
                if (data.status === 'Отклонена') {

                    $(row).addClass('denied');
                }

                // var currentDate = new Date();
                // var oneDay = 24 * 60 * 60 * 1000;
                // var dateDeadlineParts = data.deadline.split('.');
                // var dateDeadline = new Date(dateDeadlineParts.reverse().join('-'));
                

                // if (currentDate >= dateDeadline) {
                //     // Если currentDate больше или равна dateDeadline, добавьте класс red-row
                //     $(row).addClass('red-row');
                // }

                // if (dateDeadline - currentDate > 0 && dateDeadline - currentDate <= oneDay * 3) {
                //     $(row).addClass('yellow-row');
                // }

            }

            //Цветовая индикация таблиц END


        });

        $('#customSearchBox').on('keyup', function () {
            table.search(this.value).draw();
        });

        $('#table_os_length').on('change', function () {
            table.page.len($(this).val()).draw();
        });

        if (tableId === '#table_moves') {
            $(tableId + ' tbody').on('click', 'tr', function () {
                var pk = table.row(this).data().pk; // Получаем значение "pk" из строки
                if (pk) {
                    showMoveDetailsModal(pk); // Вызываем функцию для открытия модального окна с деталями
                }
            });
        }
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
        {
            "data": "pk", render: function (data, type, row) {
                return '<a href="/moves/generatemovedocument/' + data + '">Создать</a>';
            }
        }], [[3, 'desc']]
    );

    function showMoveDetailsModal(movePk) {
        $.ajax({
            url: `/moves/move_details/${movePk}`,
            success: function (data) {
                $("#move-details-content").html(data);
                $("#moveDetailsModal").css("display", "block");
            }
        });
    }

    function closeMoveDetailsModal() {
        $("#moveDetailsModal").css("display", "none");
    }

    initializeDataTable('#table_acts', '/acts/acts_list/', [
        { "data": "pk" },
        { "data": "act_date" },
        { "data": "inv_dit_id" },
        { "data": "result" },
        { "data": "conclusion" },
        { "data": "new_user_id" },
        { "data": "new_sklad_id" },
        { "data": "type" },
        { "data": "status", "visible": false },
        { "data": "avtor" },
        {
            "data": "pk",
            "render": function (data, type, row) {
                // Верните содержимое ячейки в виде HTML-кода, включая ваш блок
                return `
                    <td>
                        <div class="intable_dropdown_menu">
                            <!-- Пример: -->
                            <button id="dropdown_btn_${row.pk}" class="dropdown_menu_button" data-dropdown-id="${row.pk}">
                            <img src="/static/icons/list.svg" alt="Действия" class="dropdown_menu_button_image">
                            </button>
                            <div id="dropdown_menu_${row.pk}" class="dropdown-menu" style="display: none;">
                                <ul>
                                    <li><a href="/acts/act_edit/${data}">Изменить</a></li>
                                    <li><a href="#" onclick="confirmDelete('/acts/act_delete/${data}', '/acts/acts_list/')">Удалить</a></li>
                                    <li class="status-option" onclick="updateStatusOnActs('${row.pk}', 'True')">Выполнен</li>
                                    <li><a href="/acts/generate_act_document/${data}">Печать</a></li>
                                    <div id="dropdown_submenu_{{ acts.id }}" class="dropdown_submenu">

                                    </div>
                                </ul>
                            </div>
                        </div>
                    </td>
                `;
            }
        },

   
    ], [[0, 'desc']]
    )


    initializeDataTable('#table_applications', '/applications/applications_list/', [
        { "data": "num" },
        { "data": "requested_equipment"},
        { "data": "avtor" },
        { "data": "user" },
        { "data": "date" },
        { "data": "deadline" },
        { "data": "department" },
        {
            "data": "status",
            "render": function (data, type, row) {
                return `
                    <td>
                        <div class="intable_dropdown_menu">
                            <div class="current-status">${data}</div>
                            <div class="dropdown-menu" style="display: none;">
                                <ul>
                                    <li class="status-option">Готов к выдаче</li>
                                    <li class="status-option">Закуп</li>
                                    <li class="status-option">Необходимо заточить</li>
                                    <li class="status-option">На заточке</li>
                                    <li class="status-option">Завершена</li>
                                    <li class="status-option">Отклонена</li>
                                </ul>
                            </div>
                        </div>
                    </td>
                `;
            }
        }], [[4, 'desc']]
    );

    initializeDataTable('#table_complectations', '/complectations/complectations_list/', [
        { "data": "pk" },
        { "data": "date" },
        { "data": "avtor" },
        { "data": "inv_dit" },
        { "data": "tmc" },
        { "data": "tmc_qty" },
        { "data": "par_doc" },
    ], [[0, 'desc']]
    );

    initializeDataTable('#table_move_detail', '/move_details/<int:move_pk>', [
        { "data": "equipment_os" },
    ]);
});