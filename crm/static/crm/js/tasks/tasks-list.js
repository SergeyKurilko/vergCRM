$(document).ready(function () {
    // Получение и показ модального окна для создания новой задачи
    $('.add-new-task-button').click(function (e) { 
        e.preventDefault();
        
        $.ajax({
            type: "GET",
            url: $(this).attr("href"),
            dataType: "json",
            success: function (response) {
                console.log("Ответ от бэка")
                var modalForTaskCreate = response.new_task_modal
                $('.main_wrapper').prepend(modalForTaskCreate);

                $('#addNewTaskModal').modal("show");
            }
        });
    });

    // При закрытии модального окна для создания новой задачи, удаляем его из DOM.
    // Так же удаляем инициированные им tempus-dominus-widget и datetime-tempus-script
    $(document).on('hidden.bs.modal', '#addNewTaskModal', function () {
        $('#addNewTaskModal').remove();
        $('.tempus-dominus-widget').remove();
        $('.datetime-tempus-script').remove();
    })

    // Отправка формы для создания задачи и напоминаний
    $(document).on('submit', '#addNewTask', function (e) {
        e.preventDefault();
        var urlForCreateTask = $(this).attr('action');

        $.ajax({
            type: "POST",
            url: urlForCreateTask,
            data: $(this).serialize(),
            dataType: "json",
            success: function (response) {
                showToast(message="Задача добавлена");
                var urlForRedirectToTaskPage = response.url_for_redirect
                window.location.href = urlForRedirectToTaskPage
            },
            error: function (response) {
                var errorMessage = response.responseJSON['message']
                $('.new-task-error-place').text(errorMessage)
            }
        });
    })


    //******************************************Напоимнания*******************************************//
    function initTempusEventHandlers() {
        $('[id^="reminder-once-datetime-"], [id^="reminder-recurring-time-"]').off('change.tempus').on('change.tempus', function() {
            console.log("Дата изменена");
            validateReminderBlock($(this).attr('id').split('-')[3]);
        });
    }


    var currentReminderNumber = 1

    // Получение карточки для нового напоминания
    $(document).on('click', '#add-card-for-reminder-btn', function (e) {
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
    })

    // Выпор типа напоминания и показ его полей.
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

    // Удаление карточки с формой для нового напоминания
    $(document).on('click', '.delete-reminder-item-btn', function (e) {
        var reminderNumber = $(this).data('reminder-item')
        $(`#reminderItem-${reminderNumber}`).remove();
    })
    // Добавление напоминаний в задачах - end

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
        console.log("Что-то отследили")
        validateReminderBlock(reminderId);
    });

    // Событие изменения поля с date picker или datetime picker
    $(document).on('change', '[id^="reminder-once-datetime-"], [id^="reminder-recurring-time-"]', function () {
        const reminderId = $(this).attr('id').split('-')[3]; // Получаем ID из ID поля
        console.log("Выбран календарь")
        validateReminderBlock(reminderId);
    });

    // Событие выбора дня (дней) для recurring reminder
    $(document).on('change', '[class^="day-btn-for-"]', function () {
        const reminderId = $(this).attr('class').split('day-btn-for-')[1].split(' ')[0];
        console.log("Выбран день!")
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
    //******************************************Напоимнания - end*******************************************//
});