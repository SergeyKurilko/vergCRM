$(document).ready(function () {
    // Подтверждение удаления файла
    $('#deleteFileForm').submit(function (e) { 
        e.preventDefault();

        showDotsLoader($('.confirm-delete-file-modal-content'));

        $.ajax({
            type: "POST",
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: "json",
            success: function (response) {
                var deletedFileType = response.deleted_file_type
                var deletedFileId = response.deleted_file_id
                $('#deleteFileModal').modal('hide');
                hideDotsLoader();
                showToast("Файл удален");
                if (deletedFileType === 'image') {
                    $(`#image-item-${deletedFileId}`).fadeOut();
                } else if (deletedFileType === 'document') {
                    $(`#document-item-${deletedFileId}`).remove();
                }
            },
            error: function (response) {
                var errorMessage = response.responseJSON['message'];
                hideDotsLoader();
                showAlertToast(errorMessage);
            }
        });
    });
});