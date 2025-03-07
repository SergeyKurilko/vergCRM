$(document).ready(function () {
    
    // После закрытия модального окна, удаляем его из DOM
    $('#confirmDeleteCaseModal').on('hidden.bs.modal', function() {
        $(this).remove();
    })

    


    // Отправка подтверждения на удаление
    $('#finalDeleteCaseForm').submit(function (e) { 
        e.preventDefault();
        var csrfToken = $(this).find('input[name="csrfmiddlewaretoken"]').val();
        var caseIdForFinalDelete = $(this).find('input[name="delete_case"]').val();

        $.ajax({
            type: "DELETE",
            url: $(this).attr('action') + `?delete_case=${caseIdForFinalDelete}`,
            dataType: "json",
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function (response) {
                $('#confirmDeleteCaseModal').modal('hide');
                $(`#case_tr_${caseIdForFinalDelete}`).remove()
                showToast("Кейс себестоимости удален");
            },
            error: function (response) {
                var errorMessage = response.responseJSON['message'];
                showAlertToast(errorMessage);
            }
        });
    });
});