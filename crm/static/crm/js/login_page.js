$(document).ready(function () {

    //Валидация формы login на front-end
    function checkStringLength(str) {
        var strLength = str.length
        console.log(strLength)
    }

    // Показать - скрыть пароль
    $('#showPass').click(function() {
        if ($(this).is(':checked')){
            $('#passwordInput').attr('type', 'text')
        } else {
            $('#passwordInput').attr('type', 'password')
        }
    });

    // Отправка формы
    $('#loginForm').submit(function (e) { 
        e.preventDefault();
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val()
        
        
        $.ajax({
            type: "POST",
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: "JSON",
            headers: {
                    'X-CSRF-TOKEN': csrfToken
                },
            success: function (response) {
                var redirectUrl = response.redirect_url
                window.location.href = redirectUrl
            },
            error: function (response) {
                var errorMessage = response.responseJSON['message']
                $('.login-error-place').text(errorMessage)
            }
        });
    });
});