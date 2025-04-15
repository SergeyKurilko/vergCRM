$(document).ready(function () {
    // Открытие collapseRequestDocsList при загрузке страницы
    $('.btn-for-collapse-request-docs').click();

    // Смена текста docs-list-title при просмотре документов
    $("#collapseRequestDocsList").on('show.bs.collapse', function(e) {
        $('.docs-list-title').html(`Скрыть документы <i class="bi bi-arrow-up-circle"></i>`)
    })

    // Смена текста docs-list-title при закрытии просмотра документов
    $("#collapseRequestDocsList").on('hidden.bs.collapse', function(e) {
        $('.docs-list-title').html(`Посмотреть документы <i class="bi bi-arrow-down-circle"></i>`)
    })

    // Запрос формы для добавления файлов к заявке
    $('.add-files-button').click(function (e) { 
        e.preventDefault();
        var filesType = $(this).data('add-item-type');
        var urlForGetModalAddItemsForm = $(this).data('url-for-add-item');
        var serviceRequestId = $(this).data('service_req_id')

            $.ajax({
                type: "GET",
                url: urlForGetModalAddItemsForm,
                data: {
                    "files_type": filesType,
                    "service_request_id": serviceRequestId
                
                },
                dataType: "json",
                success: function (response) {
                    console.log("Пришел ответ от бэка")
                    var modalForAddItemsForm = response.new_content
                    $('.main_wrapper').prepend(modalForAddItemsForm);
                    $('#addFileModal').modal('show');
                }
            });
    });

    // При закрытии модального окна для для добавления файлов, удаляем окно целиком из DOM    
    $(document).on('hidden.bs.modal', '#addFileModal', function (e) {
        $('#addFileModal').remove();
    });

    // Отправка формы с добавлением файлов
    $('#addFilesForm').submit(function (e) { 
        e.preventDefault();

        $.ajax({
            type: "method",
            url: $(this).attr("action"),
            data: $(this).serialize(),
            dataType: "json",
            success: function (response) {
                console.log("Ответ от бэка")
            }
        });
    });
});