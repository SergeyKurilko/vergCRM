$(document).ready(function () {
    // При закрытии модального окна с карточкой клиента, это окно удаляется из DOM
    $(document).on('hidden.bs.modal', '#ClientDetailModal', function (e) {
        $('#ClientDetailModal').remove();
    });


    // Получение карточки клиента
    $('.client-detail-link').click(function (e) { 
        e.preventDefault();
        var urlForGetModalClientDetail = $(this).attr('href')

        $.ajax({
            type: "GET",
            url: urlForGetModalClientDetail,
            dataType: "json",
            success: function (response) {
                var modalHtml = response.modal_html

                $('.main_wrapper').prepend(modalHtml)
                $('#ClientDetailModal').modal('show')
            },
            error: function (response) {
                var errorMessage = response.responseJSON["message"]
                showAlertToast(errorMessage)
                
            }
        });
    });

});