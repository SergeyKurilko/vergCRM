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
                    window.location.reload();
                },
                error: function (response) {
                    var errorMessage = response.responseJSON['message']
                    $('.add-adress-error-place').text(errorMessage)
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

});