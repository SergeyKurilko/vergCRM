$(document).ready(function () {

    // Переключение кейсов себестоимости
    $(document).on('click', '.select_this_case', function() { 
        
        var service_id = $(this).data('request-id')
        var case_id = $(this).data('case-id')
        var csrf = $('input[name=csrfmiddlewaretoken]').val()

        $.ajax({
            type: "POST",
            url: urlForChangeCurrentCase,
            data: {"request_id": service_id, "case_id": case_id, "csrfmiddlewaretoken": csrf},
            dataType: "json",

            success: function (response) {
                var urlForUpdateContent = response.url_for_update_cost_price_list
                var elementForUpdateContent = $('.cost-price-cases-container')
                var currentTotalCost = response.current_cost_price
                var currentTotalPrice = $('.current-total-price-placeholder').html().slice(0, -2)
                contentUpdate(
                    url=urlForUpdateContent,
                    element=elementForUpdateContent,
                    params=`?ServiceRequestId=${currentServiceRequestId}`
                )
                
                // При выборе кейса, меняем в основной карточке себестоимость
                $('.request-current-cost').html(`${currentTotalCost} ₽`)
                // Рассчет новой прибыли
                var currentProfit = parseInt(currentTotalPrice, 10) - parseInt(currentTotalCost)
                $('.request-profit-placeholder').html(`${currentProfit} ₽`)

                showToast("Выбран кейс себестоимости.")
                
            }
        });
        // Обновление стоимости в основной карточке
        var currentCost = $('.current-selected-cost').html()
        console.log(parseInt(currentCost, 10))
    });

    // Обработчик события закрытия calculate-cost-price-offcanvas
    // При закрытии удаляем содержимое offcanvas
    var myOffcanvas = document.getElementById('CalculateCostPriceOffcanvas')
        myOffcanvas.addEventListener('hidden.bs.offcanvas', function () {
            console.log("offcanvas is closed")
            $('#CalculateCostPriceOffcanvas').remove();
    })

});