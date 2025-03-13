


// Переключение темы (темная / светлая)
function toggleTheme() {
    const body = document.body;
    // Проверяем текущую тему
    if (body.getAttribute('data-theme') === 'dark') {
        // Если тема темная, то переключаем на светлую
        body.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light') // Сохраняем выбор в localStorage
    } else {
        // Если тема светлая, переключаем на темную
        body.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark')
    }
}

// Функция для применения сохраненной темы при загрузке страницы
function applySavedTheme() {
    const body = document.body;
    const savedTheme = localStorage.getItem('theme'); // Получаем сохраненную тему

    if (savedTheme === 'dark') {
        // Если сохранена темная тема, применяем ее
        body.setAttribute('data-theme', 'dark');
    } else {
        // Иначе применяем светлую тему (по умолчанию)
        body.removeAttribute('data-theme');
    }
}

// Назначаем обработчик события для кнопки переключения темы
document.getElementById('theme-toggle').addEventListener('click', toggleTheme);

// Применяем сохраненную тему при загрузке страницы
document.addEventListener('DOMContentLoaded', applySavedTheme);

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