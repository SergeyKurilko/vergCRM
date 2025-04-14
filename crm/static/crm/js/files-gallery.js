$(document).ready(function () {
    console.log("Скрипт для файловой галереи")

    // Смена текста docs-list-title при просмотре документов
    $("#collapseRequestDocsList").on('show.bs.collapse', function(e) {
        console.log("Открыт колапс с доками")
        $('.docs-list-title').text('Скрыть документы')
    })

    // Смена текста docs-list-title при закрытии просмотра документов
    $("#collapseRequestDocsList").on('hidden.bs.collapse', function(e) {
        console.log("Открыт колапс с доками")
        $('.docs-list-title').text('Посмотреть документы')
    })
});