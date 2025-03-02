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

    


    // Данные для отправки на создание новой заявки
    var service_id = null;
    var service_title = null;
    var client_id = null;
    var client_name = null;

    // Выбор услуги и сохранение выбора в переменную service_id
    $('.service-select').change(function (e) { 
        e.preventDefault();
        $('#service_id').val($(this).val())
    });

    // Выбор клиента и сохранение выбора в переменную client_id
    $('.client-select').change(function (e) { 
        e.preventDefault();
        $('#client_id').val($(this).val())
    });

    // Добавление новой услуги
    $('#addNewServiceForm').submit(function (e) { 
        e.preventDefault();

        var newServiceCsrfToken = $('input[name=csrfmiddlewaretoken]').val()
        
        $.ajax({
            type: "POST",
            url: $(this).attr("action"),
            data: $(this).serialize(),
            dataType: "json",
            headers: {
                'X-CSRF-TOKEN': newServiceCsrfToken
            },

            // Получаем данные о созданном новом service
            success: function (response) {
                var newServiceTitle = response.new_service_title;
                var newServiceId = response.new_service_id;

                // Создаем новый <option>
                var newOption = $('<option>', {
                    value: newServiceId,
                    text: newServiceTitle,
                    selected: true  // Делаем его выбранным
                });

                // Добавляем новый <option> в <select>
                $('.service-select').append(newOption);

                // Обновляем выбранный элемент
                $('.service-select').trigger('change');  // Вызываем событие change

                // Зкрываем modal
                $(function () {
                    $('#newServiceModal').modal('toggle');
                });

                showToast("Услуга добавлена")
            },
            error: function (response) {
                var errorMessage = response.responseJSON['message']
                $('.new-service-error-place').text(errorMessage)
            }
        });
    });

    // Добавление нового клиента
    $('#addNewClientForm').submit(function (e) { 
        e.preventDefault();

        var newClientCsrfToken = $('input[name=csrfmiddlewaretoken]').val()
        
        $.ajax({
            type: "POST",
            url: $(this).attr("action"),
            data: $(this).serialize(),
            dataType: "json",
            headers: {
                'X-CSRF-TOKEN': newClientCsrfToken
            },
            success: function (response) {
                var newClientName = response.new_client_name;
                var newClientId = response.new_client_id;

                // Создаем новый <option>
                var newOption = $('<option>', {
                    value: newClientId,
                    text: newClientName,
                    selected: true  // Делаем его выбранным
                });

                // Добавляем новый <option> в <select>
                $('.client-select').append(newOption);

                // Обновляем выбранный элемент
                $('.client-select').trigger('change');  // Вызываем событие change

                // Зкрываем modal
                $(function () {
                    $('#newClientModal').modal('toggle');
                });

                showToast("Клиент добавлен")
            },
            error: function (response) {
                var errorMessage = response.responseJSON['message']
                $('.new-client-error-place').text(errorMessage)
            }
        });
    });

    // Отправка всех данных для создания новой заявки
    $('#CreateRequestForm').submit(function (e) { 
        e.preventDefault();

        var newServiceRequestToken = $('input[name=csrfmiddlewaretoken]').val()
        
        $.ajax({
            type: "POST",
            url: $(this).attr("action"),
            data: $(this).serialize(),
            dataType: "json",
            headers: {
                'X-CSRF-TOKEN': newServiceRequestToken
            },
            success: function (response) {
                var RedirectUrl = response.redirect_url
                window.location.href = RedirectUrl
            },
            error: function (response) {
                var errorMessage = response.responseJSON['message']
                $('.new-service-request-error-place').text(errorMessage)
            }
        });
    });


});
