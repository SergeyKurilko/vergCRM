$(document).ready(function () {

    // Получение формы создания нового кейса себестоимости
    $('#AddCostPriceCaseButton').click(function (e) { 
    e.preventDefault();

        var urlForAddCostPriceCase = $(this).data('add-case-url')
        var serviceRequestId = $(this).data('service-request-id')
        var params = `query_param=add_case&ServiceRequestId=${serviceRequestId}`

        $.ajax({
            type: "GET",
            url: urlForAddCostPriceCase,
            data: params,
            dataType: "json",
            success: function (response) {
                var AddCostCaseHtml = response.add_cost_case_html
                $('.modal-body-add-cost-price-case').html(AddCostCaseHtml)
                $('#addCostPriceCaseModal').modal('show');
            }
        });
    });




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
                var newCostPriceCaseSum = response.cost_price_case_sum
                var newSelectedCaseId = response.selected_case_id
                
                // Корректировка прибыли и себестоимости в карточке
                $('.request-current-cost').text(newCostPriceCaseSum + " ₽")
                var requestCurrentTotalPrice = parseInt($('.current-total-price-placeholder').text().slice(0, -2))
                var newProfitSum = requestCurrentTotalPrice - parseInt(newCostPriceCaseSum)
                $('.request-profit-placeholder').text(newProfitSum + " ₽")

                // Отрисовка выбранного кейса
                
                // Выбранный до смены кейс
                var oldSelectedCase = $('.selected-case')
                var oldSelectedCaseId = oldSelectedCase.data('case-id')
                var requestId = oldSelectedCase.data('request-id')
                
                var newHtmlForOldSelectedCase = `<a type="button" data-request-id="${requestId}" data-case-id="${oldSelectedCaseId}" class="select_this_case">Выбрать</a>`
                oldSelectedCase.replaceWith(newHtmlForOldSelectedCase);

                // Выбранный после смены кейс
                var newSelectedCase = $(`.select_this_case[data-case-id="${newSelectedCaseId}"]`)
                
                var newHtmlForNewSelectedCase = `<span data-request-id="${requestId}" data-case-id="${newSelectedCaseId}" class="selected-case" style="color: green"><i class="bi bi-check-circle"></i></span>`
                newSelectedCase.replaceWith(newHtmlForNewSelectedCase)
                
            }
        });
    });

    // Удаление кейса себестоимости
    $('.delete-case-button').click(function (e) { 
        e.preventDefault();

        var caseIdForDelete = $(this).data('case-id')
        var params = `case_id=${caseIdForDelete}`

        // Запрос окна подтверждения удаления
        $.ajax({
            type: "GET",
            url: urlForDelCase,
            data: params,
            dataType: "json",
            success: function (response) {
                var modalForConfirmDeletHtml = response.confirm_delete_case_modal_html
                $('.main_wrapper').prepend(modalForConfirmDeletHtml);

                // Открываем новый modal
                $('#confirmDeleteCaseModal').modal('show')
            },
            error: function (response) {
                var errorMessage = response.responseJSON['message'];
                showAlertToast(errorMessage);
            }
        });
    });


});