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

    // При закрытии модального окна для добавления файлов, удаляем окно целиком из DOM    
    $(document).on('hidden.bs.modal', '#addFileModal', function (e) {
        $('#addFileModal').remove();
    });

    // Отправка формы с добавлением файлов
    $(document).on('submit', '#addFilesForm', function (e) {
        e.preventDefault();
        showDotsLoader($('.add-files-modal-content'));

        var formData = new FormData(this)

        $.ajax({
            type: "POST",
            url: $(this).attr("action"),
            data: formData,
            processData: false,  // Не обрабатывать данные
            contentType: false,  // Не устанавливать тип контента
            dataType: "json",
            success: function (response) {
                $('#addFileModal').modal('hide');
                hideDotsLoader();
                showToast("Файлы добавлены")
                

                if (response.files_type === "documents") {
                    var actualDocsListHtml = response.actual_files_list_htm
                    $('#collapseRequestDocsList').html(actualDocsListHtml)
                } else if (response.files_type === "images") {
                    var actualImagesListHtml = response.actual_files_list_htm
                    $('.images-collection').html(actualImagesListHtml)
                }
            },
            error: function (response) {
                var errorMessage = response.responseJSON['message'];
                hideDotsLoader();
                showAlertToast(errorMessage);
            }
        });
    })

    // ********************************* Удаление файла ******************************* //
    $(document).on('click', '.delete-file-btn', function (e) {
        var fileType = $(this).data('file-type')
        var fileId = $(this).data('file-id')
        
        $.ajax({
            type: "GET",
            url: $(this).data('delete-file-url'),
            data: {
                "file_type": fileType,
                "file_id": fileId
            },
            dataType: "json",
            success: function (response) {
                console.log("Получили ответ от бека.")
                var modalForDeleteFile = response.modal_for_delete_file
                $('.main_wrapper').prepend(modalForDeleteFile);
                $('#deleteFileModal').modal('show');
            }
        });
    });

    // При закрытии модального окна для подтверждения удаления файла, удаляем  модальное окно целиком из DOM    
    $(document).on('hidden.bs.modal', '#deleteFileModal', function (e) {
        $('#deleteFileModal').remove();
    });


});