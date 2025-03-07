function toggleReadonlyInput(input_id) {
    var input_item = $(`#${input_id}`)
    if (input_item.attr('readonly')) {
        input_item.removeAttr('readonly');
        input_item.focus();
        input_item.removeClass('text-muted');
    } else {
        input_item.attr('readonly', true);
        input_item.addClass('text-muted');
    }
}

// Функция для подсчета суммы
function calculateTotalCostPrice() {
    let total = 0;

    $('input[id^="part_price_"]').each(function() {
        let value = parseInt($(this).val()) || 0;
        total += value;
    });

    $('.total_cost_price_val').text(total);
    $('#total_cost_price').val(total);
}

// Инициализация суммы при загрузке страницы
calculateTotalCostPrice();

// Обработчик изменения значений в полях part_price
$(document).on('input', 'input[id^="part_price_"]', function() {
    calculateTotalCostPrice();
});


