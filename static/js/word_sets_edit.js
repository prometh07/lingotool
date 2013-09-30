$(document).ready(function() {
    $('#id_file').blur(function() {
        $(this).val() ?
            $('#id_text').prop('disabled', true) :
            $('#id_text').prop('disabled', false);
    });
    $("#id_text").blur(function() {
        $(this).val() ?
            $('#id_file').prop('disabled', true) :
            $('#id_file').prop('disabled', false);
    });
});
