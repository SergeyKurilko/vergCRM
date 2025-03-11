var editMode = false;
var newPartItemCounter = 1;
var existing_parts_have_been_modified = false;
var hasChanges = false;

var partsForDeleteSet = new Set();

// Функция включения режима редактирования
function offOnEditMode() {
    if (!editMode) {
        $('.editPartItem').addClass('d-none');
        $('#add-new-part-btn').addClass('d-none');
        $('.confirm-edit-cost-price-case-buttons').addClass('d-none');
        $('.delete-cost-part-button').addClass('d-none');
        $('.cost-price-case-detail-modal-content').removeClass('cost-price-case-edit-mode')
        $('.edit-mode-title').addClass('d-none');
        $('#OnEditModeBtn').removeClass('d-none')
        editMode = true
    } else {
        $('.editPartItem').removeClass('d-none');
        $('#add-new-part-btn').removeClass('d-none');
        $('.confirm-edit-cost-price-case-buttons').removeClass('d-none');
        $('.delete-cost-part-button').removeClass('d-none');
        $('.cost-price-case-detail-modal-content').addClass('cost-price-case-edit-mode')
        $('.edit-mode-title').removeClass('d-none');
        $('#OnEditModeBtn').addClass('d-none')
        editMode = false
    }
}


// Функция добавления новой строки new_part_item
function addNewPartItem() {
    var newPartHtml = `
    <tr id="new_part_item_${newPartItemCounter}">
        <td><input 
        type="text" 
        name="new_part_title_${newPartItemCounter}" 
        id="new_part_title_${newPartItemCounter}" 
        required 
        placeholder="название позиции" 
        class="form-control">
        </td>
        <td><input 
        type="number" 
        name="new_part_price_${newPartItemCounter}" 
        id="new_part_price_${newPartItemCounter}"
        required 
        placeholder="стоимость" 
        class="form-control">
        </td>
        <td></td>
        <td>
        <input 
        type="button" 
        data-new-part-item-tr="new_part_item_${newPartItemCounter}"
        id="" 
        value="удалить" 
        class="form-control delete-new-part-button" 
        style="color: red">
        </td>
    </tr>
    `
    hasChanges = true
    $(newPartHtml).insertBefore('.add-new-part-tr');
    newPartItemCounter += 1;
}


// Функция переключения readonly для part_price и part_title inputs.
function toggleReadonlyInput(part_id) {
    var part_title_input = $(`#part_title_${part_id}`)
    var part_price_input = $(`#part_price_${part_id}`)
    hasChanges = true

    if (part_title_input.attr('readonly') && part_price_input.attr('readonly')) {
        part_title_input.removeAttr('readonly');
        part_price_input.removeAttr('readonly')
        part_title_input.focus();
        part_title_input.removeClass('text-muted').addClass('edit_part_inputs_focus');
        part_price_input.removeClass('text-muted').addClass('edit_part_inputs_focus');
        $(`#edit_part_btn_${part_id}`).val('ок ✓')
            .removeClass('verg-input-button-1')
            .addClass('verg-green-input-btn')
    } else {
        part_title_input.attr('readonly', true).removeClass('edit_part_inputs_focus');
        part_price_input.attr('readonly', true).removeClass('edit_part_inputs_focus');
        part_title_input.addClass('text-muted');
        part_price_input.addClass('text-muted');
        $(`#edit_part_btn_${part_id}`).val('редактировать')
            .removeClass('verg-green-input-btn')
            .addClass('verg-input-button-1')
    }
}

// Функция переключения readonly для case_title input.
function toggleReadonlyCaseTitleInput () {
    var case_title_input = $('#case_detail_title')
    hasChanges = true

    if (case_title_input.attr('readonly')) {
        case_title_input.removeAttr('readonly');
        case_title_input.focus();
        case_title_input.removeClass('text-muted').addClass('edit_part_inputs_focus');
        $(`#editCaseTitle`).val('ок ✓')
            .removeClass('verg-input-button-1')
            .addClass('verg-green-input-btn')
    } else {
        case_title_input.attr('readonly', true).removeClass('edit_part_inputs_focus');
        case_title_input.addClass('text-muted');
        $(`#editCaseTitle`).val('редактировать')
            .removeClass('verg-green-input-btn')
            .addClass('verg-input-button-1')
    }
}

// Функция для подсчета суммы в cost price case detail
function calculateTotalCostPrice() {
    let total = 0;
    console.log("Считаем цену")

    $('input[id^="part_price_"]').each(function() {
        let value = parseInt($(this).val()) || 0;
        total += value;
    });

    $('input[id^="new_part_price_"]').each(function() {
        let value = parseInt($(this).val()) || 0;
        total += value;
    });

    $('.total_cost_price_val').text(total);
    $('#total_cost_price').val(total);
}

// Функуия проверки, есть ли новые parts в форме
function checkNewPartsQuantity() {
    var has_more_new_parts = $('[id^="new_part_item_"]').length > 0;
    return has_more_new_parts
}

// Функция проверки изменения общей стоимости кейса
function checkTotalPriceChanges() {
    var realTotalPrice = $('.total_cost_price_val').text()
    return currentCaseTotalPrice != parseInt(realTotalPrice, 10)
}


// Обработчик события закрытия модального окна подтверждения отмены внесения изменений
$('#confirmCancelChangesModal').on('hidden.bs.modal', function () {
    $('.cost-price-case-detail-modal-content').css("opacity", "1");
});

// Инициализация суммы при загрузке страницы
calculateTotalCostPrice();

// Обработчик нажатия кнопки "редактировать" для parts inputs
$('.editPartItem').click(function (e) { 
    e.preventDefault();
    existing_parts_have_been_modified = true;
    var part_id = $(this).data('part-id')
    toggleReadonlyInput(part_id)
});

// Обработчик нажатия кнопки "редактировать" для case title
$('#editCaseTitle').click(function (e) { 
    e.preventDefault();
    toggleReadonlyCaseTitleInput();
});

// Обработчик для кнопки "Добавить +"
$('#add-new-part-btn').click(function (e) { 
    e.preventDefault();
    addNewPartItem()
});

// Удаление новой строки new_part_item
$(document).on('click', '.delete-new-part-button', function() {
    var new_part_item_tr_id = $(this).data('new-part-item-tr')
    $(`#${new_part_item_tr_id}`).remove();
    calculateTotalCostPrice()
});


// Отправка формы для редактирования cost price case
$('#detailCostPriceCaseForm').submit(function (e) { 
    e.preventDefault();
    
    // Получаем данные формы в виде массива
    let formData = $(this).serializeArray();

    // Добавляем новый параметр
    formData.push({
        name: 'existing_parts_have_been_modified',
        value: existing_parts_have_been_modified,
    });
    formData.push({
        name: "has_new_parts",
        value: checkNewPartsQuantity(),
    });
    formData.push({
        name: "total_price_has_been_changed",
        value: checkTotalPriceChanges(),
    });
    formData.push({
       name: "for_delete_ids",
       value: Array.from(partsForDeleteSet)
    });

    // Преобразуем массив обратно в строку запроса
    let serializedData = $.param(formData);

    $.ajax({
        type: "POST",
        url: $(this).attr('action'),
        data: serializedData,
        dataType: "json",
        success: function (response) {
            var caseId = response.case_id
            var urlForUpdateContent = response.url_for_update_cost_price_list
            var elementForUpdateContent = $('.cost-price-cases-container')
            var caseIsCurrent = response.case_is_current
            var currentTotalCost = response.current_cost_price
            var currentTotalPrice = $('.current-total-price-placeholder').html().slice(0, -2)
            $('#costPriceDetailModal').modal('hide');

            contentUpdate(
                url=urlForUpdateContent, 
                element=elementForUpdateContent, 
                params=`?ServiceRequestId=${currentServiceRequestId}`
            )
            showToast("Кейс себестоимости обновлен")
            if (caseIsCurrent) {
                // Если был обновлен выбранный кейс, то корректируем стоимость в карточке заявки
                $('.request-current-cost').html(`${currentTotalCost} ₽`)
                // Рассчет новой атуальной прибыли
                var currentProfit = parseInt(currentTotalPrice, 10) - parseInt(currentTotalCost)
                $('.request-profit-placeholder').html(`${currentProfit} ₽`)
            };
        },
        error: function (response) {
            var errorMessage = response.responseJSON['message'];
            showAlertToast(errorMessage);
        }
    });  
});



// Пометка на ужаление существующих parts
$('.delete-cost-part-button').click(function (e) { 
    e.preventDefault();
    var idForDelete = $(this).data('part-id')

    if (!partsForDeleteSet.has(idForDelete)) {
        partsForDeleteSet.add(idForDelete);
        $(this).val('отмена');
        $(`.part-item_${idForDelete}`).addClass('marked-for-deletion-part')
        $(`input[name="part_title_${idForDelete}"]`).attr('name', `del_part_${idForDelete}`)

        // Вычитаем из общей суммы себестоимости помеченный на удаление part

        var nowTotalPrice = parseInt($('.total_cost_price_val').text(), 10)
        var thisPrice = parseInt($(`input[name="part_price_${idForDelete}"]`).val(), 10)
        $('.total_cost_price_val').html(`${nowTotalPrice - thisPrice}`)

    } else {
        partsForDeleteSet.delete(idForDelete);
        $(this).val('удалить');
        $(`.part-item_${idForDelete}`).removeClass('marked-for-deletion-part')
        $(`input[name="del_part_${idForDelete}"]`).attr('name', `part_title_${idForDelete}`)

        var nowTotalPrice = parseInt($('.total_cost_price_val').text(), 10)
        var thisPrice = parseInt($(`input[name="part_price_${idForDelete}"]`).val(), 10)
        $('.total_cost_price_val').html(`${nowTotalPrice + thisPrice}`)
    }
    console.log("Список ids для удаления: " + Array.from(partsForDeleteSet))
});