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

    initializeDataTable('#table_moves', '/moves/', [
        { "data": "move_num" },
        { "data": "move_date" },
        { "data": "status" },
        { "data": "avtor" },
        { "data": "sklad" },
        { "data": "user" },
        { "data": "comment" }
    ]);
});