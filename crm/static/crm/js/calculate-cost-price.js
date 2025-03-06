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

});