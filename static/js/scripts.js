var csrf_token = null;
var host = 'http://' + document.domain + ':8000';

function getMyQueries() {
    var request_path = host + '/queries/my/';
    $.post(
        request_path,
        {csrfmiddlewaretoken: csrf_token},
        function (data) {
            if (data.hasOwnProperty('queries')) {
                renderQueries(data['queries']);
            }
        }
    );
}

function renderQueries(queries) {
    var div = $("#queries");
    queries.forEach(function (query) {
        renderQuery(query, div, true);
    });
    $('.delete-query').click(lnkDeleteQueryHandler);
}

function renderQuery(query, container, append) {
    var div = $('<div>', {
        "class": "query",
        'id': 'q' + query.id
    }).append(
        $('<div>', {}).append($('<span>', {
                'class': 'txt-a-justify',
                'text': query.title
            })
        ).prepend(
            $('<i>', {
                'class': 'small-font fa ' + (query.is_public ? "fa-users" : "fa-lock"),
                'html': '&nbsp;'
            })
        ).append(
            $('<div>', {
                'class': 'query-controls'
            }).append(
                $('<a>', {
                    'href': "#",
                    'class': 'edit-query',
                    'id': query.id,
                    'text': 'Edit '
                })
            ).append(
                $('<a>', {
                    'href': "#",
                    'class': 'delete-query',
                    'id': query.id,
                    'text': 'Delete'
                })
            )
        )
    );

    div.append(
        $('<div>', {
            'class': 'query-body'
        }).append(
            $('<div>', {
                'text': query.body
            })
        ).append(
            $('<div>', {
                'class': 'query-date',
                'text': 'Added: ' + query.date
            })
        )
    );


    if (append) {
        container.append(div);
    } else {
        container.prepend(div);
    }
}

function notification(msg, type, id, close_button) {
    var notice = $('<div>', {
        'class': 'notice ' + type,
        'id': id
    });

    notice.append($('<i>', {
        'class': ('fa ' + (type == 'success' ? 'fa-check' : 'fa-times'))
    }));

    notice.append($('<span>', {
        'text': msg
    }));

    if (close_button) {
        notice.append($('<a>', {
            'class': 'fa fa-close',
            'href': '#close'
        }));
    }

    return notice;
}

function btnCreateQueryClickHandler() {
    var request_path = host + "/queries/new/";
    $.post(
        request_path,
        {
            csrfmiddlewaretoken: csrf_token,
            title: $("#title").val(),
            body: $('#body').val(),
            is_public: $('#access').val()
        },
        function (data) {
            var message = notification(data.message, data.status, "3000msNotice", false);
            $("#status-message").empty().append(message);
            message.delay(3000).fadeOut();
            if (data.status == 'success') {
                $('#title').prop("value", "");
                $('#body').prop("value", "");
                renderQuery(data.query, $("#queries"), false);
            }
        }
    );
}

function lnkDeleteQueryHandler() {
    if (!confirm('Are you sure?')) return false;
    var request_path = host + '/queries/delete/';
    var id = $(this).prop('id');
    $.post(
        request_path,
        {
            csrfmiddlewaretoken: csrf_token,
            id: id
        },
        function (response) {
            console.log(response);
            if (response.status == 'success') {
                $("#q" + id).remove();
            }
        }
    );

}

$(document).ready(function () {
    csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $('#btn-create-query').click(btnCreateQueryClickHandler);
    getMyQueries();
});