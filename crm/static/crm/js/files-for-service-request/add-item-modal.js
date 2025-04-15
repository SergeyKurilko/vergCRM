$(document).ready(function () {
    let currentFileInputNumber = 2
    let fileTypes = $(`input[name="files_type"]`).val();
    let acceptExtensions = null;
    console.log("In fileTypes: " + fileTypes)
    if (fileTypes === "documents") {
        console.log("Сработало условие: fileTypes === documents")
        acceptExtensions = `.doc,.docx,.xls,.xlsx,.ods,.pdf`
    } else if (fileTypes === "images") {
        console.log("Сработало условие: fileTypes === images")
        acceptExtensions = `.jpg,.jpeg,.png`
    }

    // Функция добавления новго инпута
    function addFileInput() {
        var newInput = `
        <div class="file-input mt-1" id="file-input-${currentFileInputNumber}">
            <input name="file_${currentFileInputNumber}" type="file" class="form-control me-1" id="file_${currentFileInputNumber}" accept=${acceptExtensions}>
            <button data-input-id="file-input-${currentFileInputNumber}" type="button" class="btn btn-danger remove-file-input border-0">Удалить</button>
        </div>
        `
        $('.files-inputs-place').append(newInput);
        currentFileInputNumber += 1
        console.log();
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