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

    // var checkboxes = document.querySelectorAll('input[name="reminderMode"]');
    // var customReminderCheckbox = document.getElementById('customReminderModeCheckInput')

    // checkboxes.forEach(function (checkbox) {
    //     checkbox.addEventListener('change', function () {
    //         if (this === customReminderCheckbox) {
    //             $('.custom-reminder-params').removeClass('d-none')
    //         } else {
    //             $('.custom-reminder-params').addClass('d-none');
    //             $('.day-btn').prop('checked', false);
    //         }
    //     })
    // })

    var currentReminderNumber = 1

    // Получение карточки для 
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




    // $(document).on("change", '[id^="recurringReminderModeCheckInput-"]', function () {
    //     var currentReminderModeId = this.getAttribute("id")
    //     var currentReminderNumber = currentReminderModeId.split('-')[1]
    //     console.log("Выбран тип напоминания для формы № " + currentReminderNumber)
    //     console.log("Будем убирать d-none у объекта с классом: " + `recurring-reminder-params-${currentReminderNumber}`)
    //     $(`.recurring-reminder-params-${currentReminderNumber}`).removeClass('d-none')
    // });

});