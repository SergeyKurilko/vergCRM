$(document).ready(function () {
    var editMode = false;
    var notifications_status = $('input[name="notifications_status"]');
    var notifications = $('input[name="notifications"]');
    

    if (notifications_status.val() == "ON") {
        console.log("Переключаем notification")
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

    // При закрытии модального окнас с подтверждением удаления, удаляем его.
    $(document).on('hidden.bs.modal', '#confirmDeleteTaskModal', function (e) {
        $('#confirmDeleteTaskModal').remove();
    });
    
});