


// Переключение темы (темная / светлая)
// function toggleTheme() {
//     const body = document.body;
//     // Проверяем текущую тему
//     if (body.getAttribute('data-theme') === 'dark') {
//         // Если тема темная, то переключаем на светлую
//         body.removeAttribute('data-theme');
//         localStorage.setItem('theme', 'light') // Сохраняем выбор в localStorage
//     } else {
//         // Если тема светлая, переключаем на темную
//         body.setAttribute('data-theme', 'dark');
//         localStorage.setItem('theme', 'dark')
//     }
// }

// Функция для применения сохраненной темы при загрузке страницы
// function applySavedTheme() {
//     const body = document.body;
//     const savedTheme = localStorage.getItem('theme'); // Получаем сохраненную тему

//     if (savedTheme === 'dark') {
//         // Если сохранена темная тема, применяем ее
//         body.setAttribute('data-theme', 'dark');
//     } else {
//         // Иначе применяем светлую тему (по умолчанию)
//         body.removeAttribute('data-theme');
//     }
// }

// Назначаем обработчик события для кнопки переключения темы
// document.getElementById('theme-toggle').addEventListener('click', toggleTheme);

// Применяем сохраненную тему при загрузке страницы
// document.addEventListener('DOMContentLoaded', applySavedTheme);

///////////////////////////////////////// Инициализация toast ////////////////////////////////////////
$(document).ready(function() {
    // Инициализируем toast
    var toastEl = document.getElementById('backendMessageToast');
    var toast = new bootstrap.Toast(toastEl);
});

///////////////////////////////////////// /Инициализация toast ////////////////////////////////////////


// Вызов toast
function showToast(message) {
    // Определяем toast и закрываем toast (если он уже открыт)
    var toastEl = document.getElementById('backendMessageToast');
    var toast = new bootstrap.Toast(toastEl);
    toast.hide();
    

    // Наполняем toast текстом и добавляем стили
    $('#backendMessageToast').removeClass('alert_toast').addClass('success_toast')
    $('.backend-message-toast-text').text(message);

    // Показываем toast
    toast.show();
}

// Вызов toast
function showAlertToast(message) {
    // Определяем toast и закрываем toast (если он уже открыт)
    var toastEl = document.getElementById('backendMessageToast');
    var toast = new bootstrap.Toast(toastEl);
    toast.hide();

    // Наполняем toast текстом и добавляем стили
    $('#backendMessageToast').removeClass('success_toast').addClass('alert_toast')
    $('.backend-message-toast-text').text(message);

    // Показываем toast
    toast.show();
}


///////////////////////////////////////// /Обновление контента через ajax ////////////////////////////////////////

// Обновление контента через ajax
function contentUpdate(url, element, params) {
    if (!params) {
        params = ""
    }

    // Перед отправкой запроса показываем Loader
    var loader = $('.loader');
    var overlay = $('.l-overlay');
    loader.css({"display":"block"});
    overlay.css({"display":"block"});

    $.ajax({
        type: "GET",
        url: url + params,
        dataType: "json",
        success: function (response) {
            var newContent = response.new_content
            loader.css({"display":"none"});
            overlay.css({"display":"none"});
            element.replaceWith(newContent)
        }
    });
}


///////////////////////////////////////// /Показать verg-dots-loader ////////////////////////////////////////
function showDotsLoader(elForHidden, off) {
    // Если loader выключен
    if (!off) {
        // Клонируем элемент
        var loader = $('.verg-dots-loader').first().clone();

        loader.removeClass('d-none').insertAfter(elForHidden);

        // Помечаем его активным
        loader.addClass("active-dots-loader")
    
        // Размываем контент, на который будет помещен loader
        // elForHidden.css({"filter": "blur(1.4px)", "z-index": "10"});
        // elForHidden.fadeOut();
        $('.l-overlay').css("display", "block");
        
    } else {
        $(".active-dots-loader").remove();
        $('.l-overlay').css("display", "none");
    }
}

function hideDotsLoader() {
    $(".active-dots-loader").remove();
    $('.l-overlay').css("display", "none");
}

///////////////////////////////////////// Проверка display notifications ////////////////////////////////////////
let checkInterval = 1000; // Стартовый интервал

function checkDisplayNotifications() {
    $.ajax({
        type: "GET",
        url: checkNotifications,
        dataType: "json",
        success: function(response) {
            if (response.success) {
                // Обновляем интервал
                if (response.interval) {
                    checkInterval = response.interval;
                }
                
                // Если есть уведомление и его ещё нет на странице
                if (response.notification && !$(`#notification-${response.notification_id}`).length) {
                    $('.main_wrapper').prepend(response.notification);
                    setupNotificationHandlers(response.notification_id)
                }
            }
        },
        complete: function() {
            // Перезапускаем с новым интервалом
            setTimeout(checkDisplayNotifications, checkInterval);
        }
    });
}

// Обработчик события прочтения оповещения
function setupNotificationHandlers(notificationId) {
    // DisplayNotification прочтано при переходе по ссылке в оповещении
    $(`#mark-read-link-${notificationId}`).click(function (e) { 
        e.preventDefault();
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        var successRedirectUrl = $(this).attr('href')
        console.log("csrfToken: " + csrfToken)
        console.log("Ссылка: " + $(this).attr('href'))

        var makeViewdUrl = $(this).data("url-for-make-viewed")
        $.ajax({
            url: makeViewdUrl,
            method: 'POST',
            data: {"notification_id": notificationId, "csrfmiddlewaretoken": csrfToken},
            success: function() {
                $(`#notification-${notificationId}`).remove();
                window.open(successRedirectUrl, '_blank');
            }
        });
    });

    // DisplayNotification прочитано при нажатии "Прочитано"
    $(`#mark-read-${notificationId}`).submit(function (e) {
        e.preventDefault();
 
        $.ajax({
            url: $(this).attr("action"),
            method: 'POST',
            data: $(this).serialize(),
            success: function() {
                $(`#notification-${notificationId}`).remove();
            }
        });
    });
}

// Первый запуск
$(document).ready(function() {
    checkDisplayNotifications();
});

///////////////////////////////////////// /Проверка display notifications ////////////////////////////////////////