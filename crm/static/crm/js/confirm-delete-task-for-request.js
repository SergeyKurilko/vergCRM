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
                

                // Обновляем список задач:
                var urlForUpdateTaskList = response.url_for_update_content
                contentUpdate(
                    url=`${urlForUpdateTaskList}`,
                    element=$('.task-list-for-service-request-offcanvas-body'),
                    params=`?service_request_id=${currentServiceRequestId}&filter_by=all`
                );

                showToast("Задача удалена");
            },
            error: function (response) {
                var errorMessage = response.responseJSON['message'];
                console.log(errorMessage)
                showAlertToast(errorMessage);
            }
        });
    });
});