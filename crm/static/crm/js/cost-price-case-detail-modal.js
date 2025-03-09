var editMode = false;
var newPartItemCounter = 1;
var existing_parts_have_been_modified = false;
var hasChanges = false;

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

// Функция для подсчета суммы
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

// Обработчик нажатия кнопки включения режима редактирования
$(document).on('click', '#OnEditModeBtn', function() {
    offOnEditMode();
});

// Обработчик нажатия кнопки выключения режима редактирования
$(document).on('click', '#CancelEditCostPriceCaseButton', function() {
    if (!hasChanges) {
        offOnEditMode();
    } else {
        $('#confirmCancelChangesModal').modal('show');
        $('.cost-price-case-detail-modal-content').css('opacity', 0.4)
        console.log("Были изменения. Нужно предупредить пользователя")
    }
    
});

// Обработчик события закрытия модального окна подтверждения отмены внесения изменений
$('#confirmCancelChangesModal').on('hidden.bs.modal', function () {
    $('.cost-price-case-detail-modal-content').css("opacity", "1");
});



// Инициализация суммы при загрузке страницы
calculateTotalCostPrice();

// Обработчик изменения значений в полях part_price
$(document).on('input', 'input[id^="part_price_"]', function() {
    calculateTotalCostPrice();
});

$(document).on('input', 'input[id^="new_part_price"]', function() {
    calculateTotalCostPrice();
});

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


// Отправка формы для изменения cost price case
$('#detailCostPriceCaseForm').submit(function (e) { 
    e.preventDefault();
    
    // Получаем данные формы в виде массива
    let formData = $(this).serializeArray();
    console.log("formData " + formData)

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

    // Преобразуем массив обратно в строку запроса
    let serializedData = $.param(formData);

    $.ajax({
        type: "POST",
        url: $(this).attr('action'),
        data: serializedData,
        dataType: "json",
        success: function (response) {
            var caseId = response.case_id
            $('#costPriceDetailModal').remove();
            $('.modal-backdrop').remove();
            $(`#LinkForCase${caseId}`).trigger('click')
        },
        error: function (response) {
            var errorMessage = response.responseJSON['message'];
            showAlertToast(errorMessage);
        }
    });
    
});



