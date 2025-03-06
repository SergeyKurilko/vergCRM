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
    $('.select_this_case').click(function (e) { 
        e.preventDefault();
        var service_id = $(this).data('request-id')
        var case_id = $(this).data('case-id')
        var csrf = $('input[name=csrfmiddlewaretoken]').val()

        $.ajax({
            type: "POST",
            url: urlForChangeCurrentCase,
            data: {"request_id": service_id, "case_id": case_id, "csrfmiddlewaretoken": csrf},
            dataType: "json",

            success: function (response) {
                
            }
        });
        
        
    });

});