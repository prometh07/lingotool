$.fn.editable.defaults.mode = 'inline';

$('.editable_title').editable({
    params: {
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
    },
    ajaxOptions: {
        headers: { 'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest' }
    },
});

$('.editable_word').editable({
    params: {
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
    },
    ajaxOptions: {
        headers: { 'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest' }
    },
});

$('.editable_definition').editable({
    emptytext: 'brak',
    mode: 'popup',
    params: {
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
    },
    ajaxOptions: {
        headers: { 'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest' }
    },
});

function checkSelectedCheckboxes() {
    var checked_count = $(':checked').length;    
    checked_count === 0 ?
        $('#delete, #modify').prop('disabled', true) :
        $('#delete, #modify').prop('disabled', false);
}

function toggleCheckboxes(obj, target) {
    var is_active = $(obj).hasClass('active');
    $('.mark').removeClass('active');
    $(':checkbox').each( function() { $(this).prop('checked', false); });
    is_active ? $(obj).removeClass('active') : $(obj).addClass('active');
    is_active ? 
        $(target + ' :checkbox').each( function() { $(this).prop('checked', false); }) : 
        $(target + ' :checkbox').each( function() { $(this).prop('checked', true); });
    checkSelectedCheckboxes();
}

function submitForm(obj) {
    var submit_action = $(obj).attr('id');
    $('#submit_action').val(submit_action); 
    $('#word_sets_detail_form').submit();
}

$(document).ready(function() {
    checkSelectedCheckboxes();
    $('#mark_easy').on('click', function() { toggleCheckboxes(this, 'tr.easy'); });
    $('#mark_medium').on('click', function() { toggleCheckboxes(this, 'tr.medium'); });
    $('#mark_hard').on('click', function() { toggleCheckboxes(this, 'tr.hard'); });
    $('#mark_all').on('click', function() { toggleCheckboxes(this, 'tr'); });
    $('#delete, #download_txt, #download_email').on('click', function() { submitForm(this); });
    $(':checkbox').on('click', checkSelectedCheckboxes);
});
