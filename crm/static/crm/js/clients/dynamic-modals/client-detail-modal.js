$(document).ready(function () {
    var editeMode = false

    // Перенос поинтера на 3 позицию при клике по полю
    $.fn.setCursorPosition = function(pos) {
        if ($(this).get(0).setSelectionRange) {
          $(this).get(0).setSelectionRange(pos, pos);
        } else if ($(this).get(0).createTextRange) {
          var range = $(this).get(0).createTextRange();
          range.collapse(true);
          range.moveEnd('character', pos);
          range.moveStart('character', pos);
          range.select();
        }
    };

    // Маска для телефона и whatsapp
    $("#ClientPhoneInput").click(function(){
        $(this).setCursorPosition(3);
        }).mask("+7(999) 999-9999");
    
        $("#ClientWhatsappInput").click(function(){
        $(this).setCursorPosition(3);
            }).mask("+7(999) 999-9999");

    $('input').click(function (e) { 
        if (!editeMode) {
            e.preventDefault();
            $('#editClient').addClass("verg-button-1-active")
            setTimeout(function() { 
            $('#editClient').removeClass("verg-button-1-active")
            }, 200);
        }    
    });

    // Редактирование карточки клиента
    $('#editClient').click(function (e) { 
        e.preventDefault();
        $("#ClientNameInput").removeAttr("readonly").removeClass("text-muted").addClass("border-success");
        $("#ClientPhoneInput").removeAttr("readonly").removeClass("text-muted").addClass("border-success");
        $("#ClientWhatsappInput").removeAttr("readonly").removeClass("text-muted").addClass("border-success");
        $("#ClientTelegramInput").removeAttr("readonly").removeClass("text-muted").addClass("border-success");
        $("#ClientEmailInput").removeAttr("readonly").removeClass("text-muted").addClass("border-success");

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
});