$(document).ready(function () {
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

    // При открытии документа все checkboxes с днями переключаем в checked=false
    $('.day-btn').prop('checked', false);

    // Переключение чекбоксов с выбором reminder mode
    var checkboxes = document.querySelectorAll('input[name^="reminderMode-"]');
    var customReminderCheckbox = document.getElementById('customReminderModeCheckInput')

    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            if (this.checked) {
                // Если выбран customReminderCheckbox, показываем меню с выбором дней и времени.
                if (this === customReminderCheckbox) {
                    $('.custom-reminder-params').removeClass('d-none')
                } else {
                    $('.custom-reminder-params').addClass('d-none');
                    $('.day-btn').prop('checked', false);
                }
                // Снимаем выделение с остальных
                checkboxes.forEach(function (otherCheckbox) {
                    if (otherCheckbox !== checkbox) {
                        otherCheckbox.checked = false;
                    }
                });
            } 
            // else {
            //     // Если нужно запретить снятие выделения (обязательный выбор), можно раскомментировать:
            //     // this.checked = true;
            // }
        });
    });

    // // Отслеживание нажатия customReminderModeCheckInput
    // var customReminderCheckbox = document.getElementById('customReminderModeCheckInput')
    // customReminderCheckbox.addEventListener('change', function () {
    //     if (this.checked) {
    //         console.log("Нажат режим кастомной напоминалки")
    //     }
    // })


});