$(document).ready(function () {
    var editeMode = false

    

    // Редактирование карточки клиента
    $('#editClient').click(function (e) { 
        e.preventDefault();
        $("#ClientNameInput").removeAttr("readonly").removeClass("text-muted").addClass("border-success");
        $("#ClientPhoneInput").removeAttr("readonly").removeClass("text-muted").addClass("border-success");
        $("#ClientWhatsappInput").removeAttr("readonly").removeClass("text-muted").addClass("border-success");
        $("#ClientTelegramInput").removeAttr("readonly").removeClass("text-muted").addClass("border-success");
        $("#ClientEmailInput").removeAttr("readonly").removeClass("text-muted").addClass("border-success");
        $(".delete-client-hr").removeClass('d-none');
        $("#deleteClient").removeClass('d-none');

        $(this).addClass("d-none")

        $('.confirm-edit-client-buttons').removeClass("d-none");
        editeMode = true
    });

    $('#updateClientForm').submit(function (e) { 
        e.preventDefault();
        
        $.ajax({
            type: "POST",
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: "json",
            success: function (response) {
                window.location.reload();
            },
            error: function (response) {
                var errorMessage = response.responseJSON["message"]
                $('.update-client-error-place').text(errorMessage)   
            }
        });
    });

    // Получение окна подтверждения удаления клиента
    $("#deleteClient").click(function (e) { 
        e.preventDefault();
        var urlForGetModal = $(this).data('delete-url')
        var clientId = $(this).data('client-id')

        $.ajax({
            type: "GET",
            url: `${urlForGetModal}?client_id=${clientId}`,
            dataType: "json",
            success: function (response) {
                var modalHtml = response.modal_html

                $('#ClientDetailModal').css("filter", "blur(1.4px)");

                $('.main_wrapper').append(modalHtml)
                $('#confirmDeleteClientModal').modal('show')
            },
            error: function (response) {
                var errorMessage = response.responseJSON["message"]
                showAlertToast(errorMessage)
                
            }
        });
        
    });
});