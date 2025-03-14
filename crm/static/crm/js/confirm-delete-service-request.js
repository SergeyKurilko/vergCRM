$(document).ready(function () {
    console.log("Скрипт окна подтверждения удаления заявки")

    // Подтверждение удаления заявки
    $('#finalDeleteServiceRequestForm').submit(function (e) { 
        e.preventDefault();
        $('.confirm-delete-request-modal-content').css("filter", "blur(1.5px)")
        $('.modal-footer').addClass('d-none');
        $('.delete-loader').removeClass('d-none')
        
        $.ajax({
            type: "POST",
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: "json",
            success: function (response) {
                var urlForRedirect = response.url_for_redirect
                showToast("Заявка удалена");
                setTimeout(function () {
                    window.location.replace(urlForRedirect);
                }, 700)
                
            },
            error: function (response) {
                var errorMessage = response.responseJSON['message'];
                console.log(errorMessage)
                showAlertToast(errorMessage);
            }
        });
    });
});