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
        $('.complete-or-open-new-tab').addClass('d-none')
        }
    };


    // Включение режима редактирования
    $('#editTaskForRequest').click(function (e) { 
        e.preventDefault();
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

    //******************************************Напоимнания*******************************************//
    function initTempusEventHandlers() {
        $('[id^="reminder-once-datetime-"], [id^="reminder-recurring-time-"]').off('change.tempus').on('change.tempus', function() {
            validateReminderBlock($(this).attr('id').split('-')[3]);
        });
    }

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
                initTempusEventHandlers(); 
            }
        });
    });

    // Валидация полей напоминания
    // Показ сообщения об ошибке
    function showError(element, message) {
        let errorElement = element.next('.error-message');
        if (!errorElement.length) {
            errorElement = $(`<div class="error-message text-danger mt-1">${message}</div>`);
            element.after(errorElement);
        }
        element.addClass('is-invalid');
    }

    // Скрытие сообщения об ошибке
    function hideError(element) {
        element.next('.error-message').remove();
        element.removeClass('is-invalid');
    }

    // Валидация при изменении полей

    // Событие выбора типа напоминания
    $(document).on('change', '[id^="onceReminderModeCheckInput-"], [id^="recurringReminderModeCheckInput-"]', function () {
        const reminderId = $(this).attr('id').split('-')[1];
        validateReminderBlock(reminderId);
    });

    // Событие изменения поля с date picker или datetime picker
    $(document).on('change', '[id^="reminder-once-datetime-"], [id^="reminder-recurring-time-"]', function () {
        const reminderId = $(this).attr('id').split('-')[3]; // Получаем ID из ID поля
        validateReminderBlock(reminderId);
    });

    // Событие выбора дня (дней) для recurring reminder
    $(document).on('change', '[class^="day-btn-for-"]', function () {
        const reminderId = $(this).attr('class').split('day-btn-for-')[1].split(' ')[0];
        validateReminderBlock(reminderId);
    });

    // Валидация конкретного блока напоминания
    function validateReminderBlock(reminderId) {
        // Сбрасываем все ошибки в блоке
        $(`#reminderItem-${reminderId} .is-invalid`).removeClass('is-invalid');
        $(`#reminderItem-${reminderId} .error-message`).remove();

        // Проверка разового напоминания
        if ($(`#onceReminderModeCheckInput-${reminderId}`).is(':checked')) {
            const datetimeInput = $(`#reminder-once-datetime-${reminderId}`);
            if (!datetimeInput.val()) {
                showError(datetimeInput, 'Укажите дату и время для разового напоминания');
            }
        }

        // Проверка повторяющегося напоминания
        if ($(`#recurringReminderModeCheckInput-${reminderId}`).is(':checked')) {
            const timeInput = $(`#reminder-recurring-time-${reminderId}`);
            let hasDaysChecked = false;

            $(`.day-btn-for-${reminderId}`).each(function () {
                if ($(this).is(':checked')) {
                    hasDaysChecked = true;
                    return false;
                }
            });

            if (!timeInput.val()) {
                showError(timeInput, 'Укажите время для повторяющегося напоминания');
            }

            if (!hasDaysChecked) {
                showError($(`#reminderItem-${reminderId} .days-btn-container`), 'Выберите хотя бы один день');
            }
        }
    }

    // Удаление reminder
    $('.confirm-delete-reminder').click(function (e) { 
        e.preventDefault();

        var urlForDeleteReminder = $(this).data('url-for-delete-reminder')
        var reminerId = $(this).data('delete-existing-reminder')

        $.ajax({
            type: "GET",
            url: urlForDeleteReminder,
            data: `reminder_id=${reminerId}`,
            dataType: "json",
            success: function (response) {
                $(`.existing-reminder[id="reminder${reminerId}"]`).remove();
                showToast(message="Напоминание удалено")
            }
        });
        
    });

    //******************************************Напоимнания - end*******************************************//

    
    
});