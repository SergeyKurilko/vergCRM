$(document).ready(function () {
    var editMode = false;
    var notifications_status = $('input[name="notifications_status"]');
    var notifications = $('input[name="notifications"]');

    // Проверка состояния notification у задачи
    if (notifications_status.val() == "ON") {
        notifications.prop('checked', true)
    }

    // Функция переключения в режим редактирования.
    function toggleEditMode() {

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

    // Отмена режима редактирования
    $('.cancel-task-changes').click(function (e) {
        e.preventDefault();
        window.location.reload();
    });

    // Отправка формы отредактированной задачи
    $('#updateTask').submit(function (e) { 
        e.preventDefault();
        var urlForUpdateTask = $(this).attr('action')

        $.ajax({
            type: "POST",
            url: urlForUpdateTask,
            data: $(this).serialize(),
            dataType: "json",
            success: function (response) {
                showToast(message="Задача изменена");
                window.location.reload()
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
                $('#TaskForRequestDetailModal').css({ "filter": "blur(4px)" });
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
                $('.task-detail-container').after(newContent);
                $('#confirmDeleteTaskModal').modal('show');
                // $('#TaskForRequestDetailModal').css({"filter":"blur(4px)"});
            },
            error: function (response) {
                var errorMessage = response.responseJSON['message']
                $('.update-task-error-place').text(errorMessage)
            }
        });
    });

    // При закрытии модального окна с подтверждением удаления, удаляем его.
    $(document).on('hidden.bs.modal', '#confirmDeleteTaskModal', function (e) {
        $('#confirmDeleteTaskModal').remove();
    });

    //******************************************Напоимнания*******************************************//
    function initTempusEventHandlers() {
        $('[id^="reminder-once-datetime-"], [id^="reminder-recurring-time-"]').off('change.tempus').on('change.tempus', function () {
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

    // Отслеживание выбора типа нового напоминания, показ необходимых полей для него
    $(document).on("change", '[class^="verg-green-checkbox-input"]', function () {
        var currentReminderModeId = this.getAttribute("id")
        var currentReminderNumber = currentReminderModeId.split('-')[1]

        if ($(this).hasClass('recurring-inputs') && $(this).prop("checked", true)) {
            $(`.recurring-reminder-params-${currentReminderNumber}`).removeClass('d-none')
            $(`.once-reminder-params-${currentReminderNumber}`).addClass('d-none');
            $(`input[name="reminder_once_datetime-${currentReminderNumber}"]`).val('');
        } else if ($(this).hasClass('once-inputs') && $(this).prop("checked", true)) {
            $(`.recurring-reminder-params-${currentReminderNumber}`).addClass('d-none');
            $(`.day-btn-for-${currentReminderNumber}`).prop("checked", false);
            $(`input[name="reminder_recurring_time-${currentReminderNumber}"]`).val('');
            $(`.once-reminder-params-${currentReminderNumber}`).removeClass('d-none');
        }
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

    // Удаление карточки с формой для нового напоминания
    $(document).on('click', '.delete-reminder-item-btn', function (e) {
        var reminderNumber = $(this).data('reminder-item')
        $(`#reminderItem-${reminderNumber}`).remove();
    })

    // Удаление существующего reminder
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
                showToast(message = "Напоминание удалено")
            }
        });

    });

    //******************************************Напоимнания - end*******************************************//

});