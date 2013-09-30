function toggleCheckboxes(obj) {
    $(obj).toggleClass('active');
    $(':checkbox').each( function() { 
        $(this).prop('checked') ? 
            $(this).prop('checked', false) :
            $(this).prop('checked', true);
    });
}

function submitForm(obj) {
    var submit_action = $(obj).attr('id');
    $('#submit_action').val(submit_action); 
    $('#word_sets_list_form').submit();
}

$(document).ready(function() {
    $('#mark_all').on('click', function() { toggleCheckboxes(this); });
    $('#delete, #merge, #download_txt, #download_email').on('click', function() { submitForm(this); });
});
