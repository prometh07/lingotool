checkSelectedCheckboxes = function() {
    var checked_count = $(':checked').length;    
    checked_count === 0 ?
        $('#delete, #download').prop('disabled', true) :
        $('#delete, #download').prop('disabled', false);
    checked_count < 2 ?
        $('#merge').prop('disabled', true) :
        $('#merge').prop('disabled', false);
}

toggleCheckboxes = function(obj) {
    $(obj).toggleClass('active');
    $(':checkbox').each( function() { 
        $(this).prop('checked') ? 
            $(this).prop('checked', false) :
            $(this).prop('checked', true);
    });
    checkSelectedCheckboxes();
}

submitForm = function(obj) {
    var submit_action = $(obj).attr('id');
    $('#submit_action').val(submit_action); 
    $('#word_sets_list_form').submit();
}

setScrollableTableHeight = function() {
    var toolbar_height = $('#toolbar').height();
    var form_height = $('#content').height();
    $('#table-body').height(form_height - toolbar_height - 20);
}

$(document).ready(function() {
    setScrollableTableHeight();
    checkSelectedCheckboxes();
    $('#mark_all').on('click', function() { toggleCheckboxes(this); });
    $('#delete, #merge, #download_txt, #download_email').on('click', function() { submitForm(this); });
    $(':checkbox').on('click', checkSelectedCheckboxes);
});
