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
        console.log("Добавить строку")
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
                var caseTitle = response.case_title
                var casePrice = response.case_price
                var caseId = response.cost_price_case_id
                var requestId = response.service_request_id

                var htmlForNewCase = `
                    <tr>
                        <td>${caseTitle}</td>
                        <td>${casePrice}</td>
                        <td><span data-request-id="${requestId}" data-case-id="${caseId}" class="selected-case" style="color: green"><i class="bi bi-check-circle"></i></span></td>
                    </tr>
                `

                $('.modal-body-add-cost-price-case').html('')
                $('#addCostPriceCaseModal').modal('hide');
                $('.cost-price-cases-table').removeClass('d-none')
                
                currentSelectedCase.html(`<a type="button" data-request-id="${requestId}" data-case-id="${currentSelectedCaseId}" class="select_this_case">Выбрать</a>`)
                $('.cost-price-cases').append(htmlForNewCase);

                $('.request-current-cost').text(casePrice + " ₽")
                var currentRequestPriceText = $('.current-total-price-placeholder').text()
                var currentRequestPriceInt = parseInt(currentRequestPriceText.slice(0, -2).trim(), 10);
                var newCurrentProfit = currentRequestPriceInt - casePrice

                $('.request-profit-placeholder').text(newCurrentProfit + " ₽")
            }
        });
    });

    $('#CancelCreateCostPriceCaseButton').click(function (e) { 
        e.preventDefault();
        $('#addCostPriceCaseModal').modal('hide');
    });
});