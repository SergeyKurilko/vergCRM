$(document).ready(function () {
    
    // Финальное подтверждение удаления клиента
    $("#finalDeleteClient").submit(function (e) { 
        e.preventDefault();
        showDotsLoader(this)

        var clientId = $(`#finalDeleteClient input[name="client_id"]`).val()

        
        $.ajax({
            type: "POST",
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: "json",
            success: function (response) {
                // window.location.reload();
                $('#ClientDetailModal').modal('hide');
                $('#confirmDeleteClientModal').modal('hide');
                showDotsLoader(elForHidden=this, off=true)
                $(`#client-tr-${clientId}`).fadeOut();
                $(`#client-tr-${clientId}`).remove();
            },
            error: function (response) {
                showDotsLoader(elForHidden=this, off=true)
                var errorMessage = response.responseJSON['message']
                $('.delete-client-error-place').text(errorMessage)
            }
        });
        
    });
});