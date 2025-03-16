$(document).ready(function () {
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


    // Открывание модального окна с формой создания нового клиента
    $('.add-new-client-button').click(function (e) { 
        e.preventDefault();
        $('#CreateClientModal').modal('show')
        
    });

    // Отправка формы создания нового клиента
    $("#CreateClientForm").submit(function (e) { 
        e.preventDefault();
        showDotsLoader(this)
        
        $.ajax({
            type: "POST",
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: "json",
            success: function (response) {
                window.location.reload();
            },
            error: function (response) {
                showDotsLoader(elForHidden=this, off=true)
                var errorMessage = response.responseJSON['message']
                $('.create-client-error-place').text(errorMessage)
            }
        });
    });

    // При закрытии модального окна с подтверждением удаления клиента, удаляем это окно из DOM
    // И убираем blur с его "родительского" окна.
    $(document).on('hidden.bs.modal', '#confirmDeleteClientModal', function (e) {
        $('#ClientDetailModal').css("filter", "none");
        $('#confirmDeleteClientModal').remove();
    });

});