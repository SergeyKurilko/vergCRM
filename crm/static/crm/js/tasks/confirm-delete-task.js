$(document).ready(function () {
    // Подтверждение удаления
    $('#finalDeleteTaskForm').submit(function (e) { 
        e.preventDefault();
        
        $.ajax({
            type: "POST",
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: "json",
            success: function (response) {
                $('#confirmDeleteTaskModal').modal('hide');
                $('#TaskForRequestDetailModal').modal('hide')
                

                // Переходим к общему списку задач:
                var urlForRedirect = response.url_for_redirect
                window.location.href = urlForRedirect;
            },
            error: function (response) {
                var errorMessage = response.responseJSON['message'];
                showAlertToast(errorMessage);
            }
        });
    });
});