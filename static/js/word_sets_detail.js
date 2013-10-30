$.fn.editable.defaults.mode = 'inline';

$.fn.editableform.template = '' +
'<form class="form-inline editableform">' +
    '<div class="control-group">' +
        '<div id="ajax"></div>' +
        '<div><div class="editable-input"></div><div class="editable-buttons"></div></div>' +
        '<div class="editable-error-block"></div>' +
    '</div>' +
'</form>';

$('.editable').editable({
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

openNextEditable = function(obj, reason) {
    if( $('#auto-next').hasClass('active') && (reason === 'save' || reason === 'nochange')) {
        var next = $(obj).closest('tr').next().find('.editable');
        setTimeout(function() { next.editable('show'); }, 300); 
    }
}

checkSelectedCheckboxes = function() {
    var checked_count = $(':checked').length;    
    checked_count === 0 ?
        $('#delete, #modify').prop('disabled', true) :
        $('#delete, #modify').prop('disabled', false);
}

toggleCheckboxes = function(obj) {
    var target = $(obj).attr('data-target');
    var is_active = $(obj).hasClass('active');
    $('.mark').removeClass('active');
    $(':checkbox').each( function() { $(this).prop('checked', false); });
    is_active ? $(obj).removeClass('active') : $(obj).addClass('active');
    is_active ? 
        $(target + ' :checkbox').each( function() { $(this).prop('checked', false); }) : 
        $(target + ' :checkbox').each( function() { $(this).prop('checked', true); });
    checkSelectedCheckboxes();
}

submitForm = function(obj) {
    var submit_action = $(obj).attr('id');
    $('#submit_action').val(submit_action); 
    $('#word_sets_detail_form').submit();
}

getDictionaryData = function() { 
    
};

error_f = function() { }

setScrollableTableHeight = function() {
    var toolbar_height = $('#toolbar').height();
    var form_height = $('#content').height();
    $('#table-body').height(form_height - toolbar_height - 20);
}

$(document).ready(function() {
    setScrollableTableHeight();
    checkSelectedCheckboxes();
    $('#mark_easy, #mark_medium, #mark_hard, #mark_all').on('click', 
        function() { toggleCheckboxes(this); });
    $('#delete, #download_txt, #download_email').on('click', 
        function() { submitForm(this); });
    $(':checkbox').on('click', checkSelectedCheckboxes);
    $('#auto-next').on('click', 
        function() { $(this).toggleClass('active'); });
    $('.editable_definition').on('hidden', 
        function(e, reason){ openNextEditable(this, reason); });
    $('.editable_definition').on('click', 
        function() {  
            $.ajax({
                url: $('#current_page').val(),
                type: 'POST',
                data: {
                    'word': $(this).parent().prev().text(),
                    'get_dict_data': 'true',
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },
                headers: { 'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest' },
                success: getDictionaryData,
                error: error_f
            });
        });
});
