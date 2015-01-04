csrf_token = null;

function btnCreateQueryClickHandler(){
    $.post(
        "",
        {

        },
        function(data, status) {

        }
    );
}

$(document).ready(function() {
    csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $('#btn-create-query').click(btnCreateQueryClickHandler);

});