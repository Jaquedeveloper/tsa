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

function createQueryDisplayBody(query) {
    var div = $('<div>');

    if (query.all_words) {
        div.append($('<p>', {
            'text': 'All these words: ' + query.all_words
        }))
    }

    if (query.phrase) {
        div.append($('<p>', {
            'text': 'This phrase: ' + query.phrase
        }))
    }

    if (query.any_word) {
        div.append($('<p>', {
            'text': 'Any of these words: ' + query.any_word
        }))
    }

    if (query.none_of) {
        div.append($('<p>', {
            'text': 'None of these words: ' + query.none_of
        }))
    }

    if (query.hashtags) {
        div.append($('<p>', {
            'text': 'These hashtags: ' + query.hashtags
        }))
    }

    if (query.users) {
        div.append($('<p>', {
            'text': 'From these users: ' + query.users
        }))
    }

    if (query.date_from) {
        div.append($('<p>', {
            'text': 'From this date: ' + query.date_from
        }))
    }

    if (query.date_to) {
        div.append($('<p>', {
            'text': 'To this date: ' + query.date_to
        }))
    }

    return div;
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
                    'class': 'run-query',
                    'id': query.id,
                    'text': 'Run'
                })
            ).append(
                $('<span>', {'html': '&nbsp;'})
            ).append(
                $('<a>', {
                    'href': "#",
                    'class': 'edit-query',
                    'id': query.id,
                    'text': 'Edit'
                })
            ).append(
                $('<span>', {'html': '&nbsp;'})
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
            createQueryDisplayBody(query)
        ).append(
            $('<div>', {
                'class': 'query-date',
                'text': 'Added: ' + query['date']
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
    var request_data = {
        csrfmiddlewaretoken: csrf_token,
        title: $("#title").val(),
        all_words: $('#all_words').val(),
        phrase: $('#phrase').val(),
        any_word: $('#any_word').val(),
        none_of: $("#none_of").val(),
        hashtags: $("#hashtags").val(),
        users: $("#users").val(),
        date_from: $("#df").val(),
        date_to: $("#dt").val(),
        is_public: $('#is_public').val()
    };

    if (request_data.title.length == 0) {
        $("#title").addClass('error');
        $('label[for="title"]').addClass('error');
        return false;
    }

    if (
        request_data.all_words.length == 0 && request_data.phrase.length == 0 && request_data.any_word.length == 0 &&
        request_data.none_of.length == 0 && request_data.hashtags.length == 0 && request_data.users.length == 0 &&
        request_data.date_from.length == 0 && request_data.date_to.length == 0
    ) {
        return false;
    }

    $.post(
        request_path,
        request_data,
        function (data) {
            var message = notification(data.message, data.status, "3000msNotice", false);
            $("#status-message").empty().append(message);
            message.delay(3000).fadeOut();
            if (data.status == 'success') {
                $('#title').val("");
                $('#all_words').val("");
                $('#phrase').val("");
                $('#any_word').val("");
                $("#none_of").val("");
                $("#hashtags").val("");
                $("#users").val("");
                $("#df").val("");
                $("#dt").val("");
                $('#is_public').val("");
                renderQuery(data['query'], $("#queries"), false);
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