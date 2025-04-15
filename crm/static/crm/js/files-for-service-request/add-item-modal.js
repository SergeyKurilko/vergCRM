$(document).ready(function () {
    let currentFileInputNumber = 2
    let fileTypes = $(`input[name="files_type"]`).val();
    let acceptExtensions = null;
    let allowedExtensions = null;
    if (fileTypes === "documents") {
        console.log("Сработало условие: fileTypes === documents")
        acceptExtensions = `
            application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document,
            application/vnd.ms-excel,
            application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,
            application/vnd.oasis.opendocument.spreadsheet,
            application/pdf`
            allowedExtensions = ['.doc', '.docx', '.xls', '.xlsx', '.ods', '.pdf']
        console.log("Будут доступны расширения allowedExtensions: " + allowedExtensions)
    } else if (fileTypes === "images") {
        console.log("Сработало условие: fileTypes === images")
        acceptExtensions = `image/jpeg, image/png, image/jpg`;
        allowedExtensions = ['.jpeg', '.png', '.jpg']
        console.log("Будут доступны расширения allowedExtensions: " + allowedExtensions)
    }

    // Функция добавления новго инпута
    function addFileInput() {
        var newInput = `
        <div class="file-input mt-1" id="file-input-${currentFileInputNumber}">
            <input required name="file_${currentFileInputNumber}" type="file" class="form-control me-1 file-input-item" id="file_${currentFileInputNumber}" accept="${acceptExtensions}">
            <button data-input-id="file-input-${currentFileInputNumber}" type="button" class="btn btn-danger remove-file-input border-0">Удалить</button>
        </div>
        `
        $('.files-inputs-place').append(newInput);
        currentFileInputNumber += 1
    };

    // Функция проверки количества инпутов
    function checkInputsCount() {
        var inputsCount = $('.remove-file-input').length
        if (inputsCount === 1) {
            $('.remove-file-input').attr("disabled", true)
        } else {
            $('.remove-file-input').attr("disabled", false)
        }
    }

    // Проверка допустимых расширений у файлов
    $(document).off('change', '.file-input-item').on('change', '.file-input-item', function (e) {
        // Получаем выбранный файл
        console.log("Мы меняем поле и доступны форматы allowedExtensions: " + allowedExtensions)
        var file = this.files[0];
        if (!file) return;
        
        // Проверяем расширение
        var fileName = file.name.toLowerCase();
        var fileExtension = fileName.substring(fileName.lastIndexOf('.'));
        
        if (!allowedExtensions.includes(fileExtension)) {
        alert(`Недопустимый формат файла! Разрешены только: ${allowedExtensions.join(', ')}`);
        $(this).val(''); // Очищаем поле
    }
    })

    // Добавление нового инпута для файлов
    $('.add-file-input-btn').click(function (e) { 
        e.preventDefault();
        addFileInput();
        checkInputsCount();
    });

    // Remove инпута для файлов
    $(document).on("click", ".remove-file-input", function (e) {
        e.preventDefault();
        if ($('.remove-file-input').length > 1) { 
            var fileInputIdForRemove = $(this).data("input-id");
            console.log('Нажали на удаление. fileInputIdForRemove: ' + fileInputIdForRemove)
            $(`#${fileInputIdForRemove}`).remove();
            checkInputsCount();
        }
    })

});