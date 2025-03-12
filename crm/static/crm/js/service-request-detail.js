$(document).ready(function () {
    // Добавление адреса для заявки
    $('#RequestDetailAddAdressButton').click(function (e) { 
        e.preventDefault();
        var RequestDetailAddAdressButton = $(this)
         
        // Убираем кнопку добавления адреса
        RequestDetailAddAdressButton.addClass('d-none')

        // Показываем форму добавления адреса.
        $('.add-address-form').removeClass('d-none');

        $('#RequestDetailAddAdressInput').focus();

        // Отмена изменения адреса
        $('#CancelAddAddressButton').click(function (e) { 
            e.preventDefault();
            $('#RequestDetailAddAdressInput').val('')
            $('.add-address-form').addClass('d-none');
            RequestDetailAddAdressButton.removeClass('d-none');
            $('.add-adress-error-place').text('');
        });

        // Сохранение нового адреса
        $('#AddAddressForm').submit(function (e) { 
            e.preventDefault();

            var newAddressCsrfToken = $('input[name=csrfmiddlewaretoken]').val()
            
            $.ajax({
                type: "POST",
                url: $(this).attr('action'),
                data: $(this).serialize(),
                dataType: "json",
                headers: {
                    'X-CSRF-TOKEN': newAddressCsrfToken
                },
                success: function (response) {
                    var newAddress = response.address
                    $('.address-missing-alert-placeholder').remove();
                    $('.service-request-adress-placeholder').text(newAddress)
                    $('#RequestDetailAddAdressInput').val('')
                    $('.add-address-form').addClass('d-none');
                    $('.add-adress-error-place').text('');
                    $('.change-address-button').removeClass('d-none')
                    showToast("Адрес изменен")
                    
                },
                error: function (response) {
                    var errorMessage = response.responseJSON['message']
                    $('.add-adress-error-place').text(errorMessage)
                }
            });

        });
    });

    // Созранение новой стоимости заявки
    $('#initialChangeTotalPriceButton').click(function (e) { 
        e.preventDefault();

        $('.current-total-price-placeholder').addClass('d-none');
        $('#changeTotalPriceForm').removeClass('d-none');
        $(this).removeClass('verg-button-1').addClass('verg-button-1-disabled');
        $('#newTotalPriceInput').focus();

        $('#CancelTotalPriceButton').click(function (e) { 
            e.preventDefault();
            $('#newTotalPriceInput').val('');
            $('.current-total-price-placeholder').removeClass('d-none');
            $('#changeTotalPriceForm').addClass('d-none');
            $('#initialChangeTotalPriceButton').addClass('verg-button-1').removeClass('verg-button-1-disabled');
        });

        $('#changeTotalPriceForm').submit(function (e) { 
            e.preventDefault();

            var newPriceCsrfToken = $('input[name=csrfmiddlewaretoken]').val()
            
            $.ajax({
                type: "POST",
                url: $(this).attr('action'),
                data: $(this).serialize(),
                dataType: "json",
                headers: {
                    'X-CSRF-TOKEN': newPriceCsrfToken
                },
                success: function (response) {
                    var newTotalPrice = response.new_total_price
                    var newProfit = response.new_profit
                    $('#newTotalPriceInput').val('');
                    $('.current-total-price-placeholder').removeClass('d-none');
                    $('#changeTotalPriceForm').addClass('d-none');
                    $('#initialChangeTotalPriceButton').addClass('verg-button-1').removeClass('verg-button-1-disabled');

                    $('.current-total-price-placeholder').text(newTotalPrice)
                    $('.request-profit-placeholder').text(newProfit)

                    showToast("Стоимость обновлена")
                    
                },
                error: function (response) {
                    var errorMessage = response.responseJSON['message']
                    $('.total-price-error-place').text(errorMessage)
                }
            });

        });
        
    });


    // Сохранение новой заметки для заявки
    $('#addNewNoteForm').submit(function (e) { 
        e.preventDefault();

        var newNoteCsrfToken = $('input[name=csrfmiddlewaretoken]').val()
        
        $.ajax({
            type: "POST",
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: "json",
            headers: {
                'X-CSRF-TOKEN': newNoteCsrfToken
            },
            success: function (response) {
                var newNoteId = response.new_note_id
                var newNoteText = response.new_note_text
                var newNoteCreatedAt = response.new_note_created_at
                
                // Очистим поля формы
                $('textarea[name=note_text]').val('')

                // Закрываем модальное окно
                $('#addNewNoteModal').modal('hide');

                // Убираем сообщение о том, что у заявки нет заметок
                $('.no-notes').remove()

                // Форматируем дату
                const isoDate = newNoteCreatedAt;
                const date = new Date(isoDate);
                const formattedDate = date.toLocaleString('ru-RU', {
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                });
                
                // Создаем html новой заметки в список
                var newNoteHtml = `
                <div id="note_${newNoteId}" class="note-for-service-request">
                        ${newNoteText} <br>
                        <span class="text-muted">${formattedDate}</span>
                </div>
                `
                // Вставляем новую заметку вверх списка .notes-container
                $('.notes-container').prepend(newNoteHtml);

            
                $(`#note_${newNoteId}`).addClass('wave-effect');

                // Добавляем небольшую задержку перед прокруткой
                setTimeout(() => {
                    document.querySelector(`#note_${newNoteId}`).scrollIntoView({
                        behavior: 'smooth', // Плавная прокрутка
                        block: 'center',    // Элемент будет по центру экрана
                    });
                }, 500); // Задержка 1500 мс

                showToast("Заметка добавлена")

            },
            error: function (response) {
                var errorMessage = response.responseJSON['message']
                $('.new-note-error-place').text(errorMessage)
            }
        });
    });

    // Вызов окна calculate-cost-price-offcanvas и вставка в него контента
    $('#callCulateCostPriceOffcanvasButton').click(function (e) { 
        e.preventDefault();
        var urlForCallOffcanvas = $(this).data('call-offcanvas-url')
        var serviceRequestId = $(this).data('service-request-id')
        console.log("Отправлять будем сюда: " + urlForCallOffcanvas)
        var params = `query_param=get_cases&ServiceRequestId=${serviceRequestId}`

        $.ajax({
            type: "GET",
            url: urlForCallOffcanvas,
            data: params,
            dataType: "json",
            success: function (response) {
                var htmlForOffcanvas = response.offcanvas_html
                // $('#CalculateCostPriceOffcanvas').html(htmlForOffcanvas)
                $('.main_wrapper').prepend(htmlForOffcanvas);

                // Открываем offcanvas после наполнения
                $('#CalculateCostPriceOffcanvas').offcanvas('toggle')
            }
        });    
    });


    ////////// Обработчики для динамчески добавляющегося контента ///////////////////////////////////////////
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

    function getCostPriceCaseModal(link) {
        $.ajax({
            type: "GET",
            url: link,
            dataType: "json",
            success: function (response) {
                var costPriceCaseHtml = response.cost_price_case_html
                $('.main_wrapper').prepend(costPriceCaseHtml);
                $('#costPriceDetailModal').modal('show')
            }
        });
    }

    // Функция для отмены редактирования cost price detail
    function cancelChangesCostPriceCase() {
        $('#confirmCancelChangesModal').modal('hide');
        $('#costPriceDetailModal').modal('hide');
    }

    // Обработчик нажатия отмены изменений, внесенных в cost case detail
    $(document).on('click', '.final-cancel-save-edits-for-case', function () {
        cancelChangesCostPriceCase()
    })

    // Обработчик нажатия на вызов (link) cost price case detail
    $(document).on('click', '.get-case-detail-modal', function (e) {
        e.preventDefault();
        var linkForGetModal = $(this).attr('href')
        getCostPriceCaseModal(linkForGetModal)
        }
    )

    // Обработчик события закрытия modal
    $(document).on('hidden.bs.modal', '#costPriceDetailModal', function(){
        $('#costPriceDetailModal').remove(); // При закрытии, удаляем элемент
      });

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

        // Обработчик изменения значений в полях part_price
    $(document).on('input', 'input[id^="part_price_"]', function() {
        calculateTotalCostPrice();
    });

    $(document).on('input', 'input[id^="new_part_price"]', function() {
        calculateTotalCostPrice();
    });

    // Удаление кейса себестоимости
    $(document).on('click', '.delete-case-button', function () {
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
    })

    // Получение формы создания нового кейса себестоимости
    $(document).on('click', '#AddCostPriceCaseButton', function () {
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
    })

    // Получение всех задач для заявки
    $('#getTasksForRequest').click(function (e) { 
        e.preventDefault();
        var urlForAjax = $(this).data('get-tasks-url')

        $.ajax({
            type: "GET",
            data: {"service_request_id": currentServiceRequestId},
            url: urlForAjax,
            dataType: "json",
            success: function (response) {
                var htmlAllTaskListOffcanvas = response.offcanvas_with_all_tasks_html

                // Вставляем полученный html с offcanvas в main_wrapper
                $('.main_wrapper').prepend(htmlAllTaskListOffcanvas);

                // Открываем полученный offcanvas
                $('#offcanvasAllTaskList').offcanvas('show')
            },
            error: function (response) {
                var errorMessage = response.responseJSON['message'];
                showAlertToast(errorMessage);
            }
        });
    });

    // При закрытии offcanvas со списком задач - удаление всего offcanvas
    $(document).on('hidden.bs.offcanvas', '#offcanvasAllTaskList', function () {
        $('#offcanvasAllTaskList').remove();
    })
        
});