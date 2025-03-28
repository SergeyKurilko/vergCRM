$(document).ready(function () {

    // Отправка формы для создания задачи и напоминаний
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
                    url = `${UrlForUpdateTaskList}`,
                    element = $('.task-list-for-service-request-offcanvas-body'),
                    params = `?service_request_id=${currentServiceRequestId}&filter_by=all`
                )
                showToast(message = "Задача добавлена")

            },
            error: function (response) {
                var errorMessage = response.responseJSON['message']
                $('.new-task-error-place').text(errorMessage)
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
});