$(document).ready(function () {
    console.log("Скрипт для task-detail")
    $('#addNewTaskForRequest').submit(function (e) { 
        e.preventDefault();

        var urlForCreateTask = $(this).attr('action');

        $.ajax({
            type: "POST",
            url: urlForCreateTask,
            data: $(this).serialize(),
            dataType: "json",
            success: function (response) {
                var UrlForUpdateTaskList = response.url_for_update_content
                $('#addTaskForRequestModal').modal('hide');
                contentUpdate(
                    url=`${UrlForUpdateTaskList}`,
                    element=$('.task-list-for-service-request-offcanvas-body'),
                    params=`?service_request_id=${currentServiceRequestId}&filter_by=all`
                )
                showToast(message="Задача добавлена")

            },
            error: function (response) {
                var errorMessage = response.responseJSON['message']
                $('.new-task-error-place').text(errorMessage)
            }
        });
        
    });

    var reminder = $('input[name="reminder"]')
    
    $(reminder).click(function (e) { 
        console.log(reminder.val())
    });
});