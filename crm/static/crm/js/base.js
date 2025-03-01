console.log("Базовый скрипт base")

function toggleTheme() {
    const body = document.body;
    console.log("Переключаем тему")
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