$(document).ready(function() {
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
    

    // Обработчик для кнопки "Добавить +"
    $('#add-cost-part').on('click', function() {
        // Находим последний элемент с классом cost-part-item_
        var lastItem = $('[class^="cost-part-item_"]').last();
        var lastIndex = parseInt(lastItem.attr('class').split('_')[1], 10); // Получаем текущий номер
        var newIndex = lastIndex + 1; // Увеличиваем номер на 1

        // Создаем новый HTML для строки
        var newRow = `
            <tr class="cost-part-item_${newIndex}">
                <td><input type="text" name="part_title_${newIndex}" id="part_title_${newIndex}" required placeholder="название позиции" class="form-control"></td>
                <td><input type="number" name="part_price_${newIndex}" id="part_price_${newIndex}" placeholder="стоимость" class="form-control"></td>
                <td><input type="button" value="удалить" class="form-control delete-cost-part-button"></td>
            </tr>
        `;

        // Вставляем новую строку перед кнопкой "Добавить +"
        lastItem.after(newRow);
    });


    // Обработчик для кнопки "удалить" (делегирование событий)
    $(document).on('click', '.delete-cost-part-button', function() {
        // Проверяем количество строк с классом cost-part-item_
        if ($('[class^="cost-part-item_"]').length > 1) {
            $(this).closest('tr').remove(); // Удаляем строку
            calculateTotalCostPrice(); // Пересчитываем сумму после удаления
        }
    });

    // Отправка заполненной формы с новым cost price case
    $('#addNewCostPriceCaseForm').submit(function (e) { 
        e.preventDefault();
        var urlForCreateCostPriceCase = $(this).attr('action')
        var csrfForCreateCostPriceCase = $('input[name=csrfmiddlewaretoken]').val()
        
        var currentSelectedCase = $('.selected-case')
        var currentSelectedCaseId = currentSelectedCase.data('case-id')

        $.ajax({
            type: "POST",
            url: urlForCreateCostPriceCase,
            data: $(this).serialize(),
            dataType: "json",
            headers: {
                "X-CSRF-TOKEN": csrfForCreateCostPriceCase
            },
            success: function (response) {
                var urlForUpdateContent = response.url_for_update_cost_price_list
                var elementForUpdateContent = $('.cost-price-cases-container')
                contentUpdate(
                    url=urlForUpdateContent,
                    element=elementForUpdateContent,
                    params=`?ServiceRequestId=${currentServiceRequestId}`
                )
                $('#addCostPriceCaseModal').modal('hide')
                showToast("Кейс себестоимости добавлен.")
            }
        });
    });

    $('#CancelCreateCostPriceCaseButton').click(function (e) { 
        e.preventDefault();
        $('#addCostPriceCaseModal').modal('hide');
    });
});