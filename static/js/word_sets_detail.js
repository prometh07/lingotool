function toggleCheckboxes(obj, target) {
    var is_active = $(obj).hasClass('active');
    $('.mark').removeClass('active');
    $(':checkbox').each( function() { $(this).prop('checked', false); });
    is_active ? $(obj).removeClass('active') : $(obj).addClass('active');
    is_active ? 
        $(target + ' :checkbox').each( function() { $(this).prop('checked', false); }) : 
        $(target + ' :checkbox').each( function() { $(this).prop('checked', true); });
}

$.fn.editable.defaults.mode = 'inline';

$('.editable_word').editable({
    params: {
        'csrfmiddlewaretoken': '{{ csrf_token }}'
    },
    ajaxOptions: {
        headers: { 'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest' }
    },
});

$('.editable_definition').editable({
    mode: 'popup',
    params: {
        'csrfmiddlewaretoken': '{{ csrf_token }}'
    },
    ajaxOptions: {
        headers: { 'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest' }
    },
});

$(document).ready(function() {
    $('#mark_easy').on('click', function() { toggleCheckboxes(this, 'tr.easy'); });
    $('#mark_medium').on('click', function() { toggleCheckboxes(this, 'tr.medium'); });
    $('#mark_hard').on('click', function() { toggleCheckboxes(this, 'tr.hard'); });
    $('#mark_all').on('click', function() { toggleCheckboxes(this, 'tr'); });
});
