$(document).ready(function () {
    var editMode = false
    var notifications_status = $('input[name="notifications_status"]')
    var notifications = $('input[name="notifications"]')

    if (notifications_status.val() == "ON") {
        notifications.prop('checked', true)
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
        $('.actual_notifications_status').addClass('d-none');
        $('.actual_must_be_completed_by').addClass('d-none');
        $('.add-reminder-in-task-for-request-detail').removeClass('d-none');
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

    var currentReminderNumber = 1

    // Получение карточки для нового напоминания
    $('#add-card-for-reminder-btn').click(function (e) {
        e.preventDefault();
        var urlForGetContent = $(this).data('url-for-new-reminder-card')

        $.ajax({
            type: "GET",
            url: urlForGetContent,
            data: `reminder_number=${currentReminderNumber}`,
            dataType: "json",
            success: function (response) {
                var new_reminder_card = response.new_reminder_card
                $('.add_reminder_placeholder').append(new_reminder_card);
                $(`.day-btn-for-${currentReminderNumber}`).prop('checked', false);
                currentReminderNumber += 1
            }
        });
    });

    // Удаление reminder
    $('.confirm-delete-reminder').click(function (e) { 
        e.preventDefault();
        console.log("Отслежено намерение удалить")

        var urlForDeleteReminder = $(this).data('url-for-delete-reminder')
        var reminerId = $(this).data('delete-existing-reminder')

        $.ajax({
            type: "GET",
            url: urlForDeleteReminder,
            data: `reminder_id=${reminerId}`,
            dataType: "json",
            success: function (response) {
                console.log("Напоминание удалено")

                $(`.existing-reminder[id="reminder${reminerId}"]`).remove();
            }
        });
        
    });
    
});