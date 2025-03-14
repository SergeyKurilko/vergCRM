$(document).ready(function () {
    var editMode = false
    var reminder_status = $('input[name="reminder_status"]')
    var reminder = $('input[name="reminder"]')

    if (reminder_status.val() == "ON") {
        reminder.prop('checked', true)
    }
    
    // Функция переключения в режим редактирования.
    function toggleEditMode () {
     
    if (!editMode) {
        $('input[name="title"]').removeAttr('readonly');
        $('textarea[name="text"]').removeAttr('readonly');
        $('.switch-1').removeClass('d-none');
        $('.datetime-for-task-container').removeClass('d-none');
        $('.save-task-changes').removeClass('d-none');
        $('.cancel-task-changes').removeClass('d-none');
        $('#deleteTask').removeClass('d-none');
        $('.delete-task-hr').removeClass('d-none');
        $('#editTaskForRequest').addClass('d-none');
        }
    };

    // Включение режима редактирования
    $('#editTaskForRequest').click(function (e) { 
        toggleEditMode();
    });

    // Отправка формы отредактированной задачи
    $('#updateTaskForRequest').submit(function (e) { 
        e.preventDefault();
        var urlForUpdateTask = $(this).attr('action')

        $.ajax({
            type: "POST",
            url: urlForUpdateTask,
            data: $(this).serialize(),
            dataType: "json",
            success: function (response) {
                var UrlForUpdateTaskList = response.url_for_update_content
                $('#TaskForRequestDetailModal').modal('hide');
                contentUpdate(
                    url=`${UrlForUpdateTaskList}`,
                    element=$('.task-list-for-service-request-offcanvas-body'),
                    params=`?service_request_id=${currentServiceRequestId}&filter_by=all`
                )
                showToast(message="Задача изменена")
            },
            error: function (response) {
                var errorMessage = response.responseJSON['message']
                $('.update-task-error-place').text(errorMessage)
            }
        });
    });

    // Удаление задачи для заявки
    // Запрос окна подтверждения удаления
    $('#deleteTask').click(function (e) { 
        e.preventDefault();
        var urlForDelete = $(this).data('delete-url')
        var taskId = $(this).data('task-id')

        $.ajax({
            type: "GET",
            url: `${urlForDelete}?task_id=${taskId}`,
            dataType: "json",
            success: function (response) {
                var newContent = response.new_content
                $('#TaskForRequestDetailModal').after(newContent);
                $('#confirmDeleteTaskModal').modal('show');
                $('#TaskForRequestDetailModal').css({"filter":"blur(4px)"});
            },
            error: function (response) {
                var errorMessage = response.responseJSON['message']
                $('.update-task-error-place').text(errorMessage)
            }
        });
    });

    
});