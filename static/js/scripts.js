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
}

function createQueryDisplayBody(query) {
    var table = $('<table>');

    if (query.all_words) {
        table.append(
            $('<tr>').append(
                $('<td>', {'text': 'All of these words:', 'class': 'w35pc'})
            ).append(
                $('<td>', {'text': query.all_words})
            )
        )
    }

    if (query.phrase) {
        table.append(
            $('<tr>').append(
                $('<td>', {'text': 'This phrase:', 'class': 'w35pc'})
            ).append(
                $('<td>', {'text': query.phrase})
            )
        )
    }

    if (query.any_word) {
        table.append(
            $('<tr>').append(
                $('<td>', {'text': 'Any of these words:', 'class': 'w35pc'})
            ).append(
                $('<td>', {'text': query.any_word})
            )
        )
    }

    if (query.none_of) {
        table.append(
            $('<tr>').append(
                $('<td>', {'text': 'None of these words:', 'class': 'w35pc'})
            ).append(
                $('<td>', {'text': query.none_of})
            )
        )
    }

    if (query.hashtags) {
        table.append(
            $('<tr>').append(
                $('<td>', {'text': 'These hashtags:', 'class': 'w35pc'})
            ).append(
                $('<td>', {'text': query.hashtags})
            )
        )
    }

    if (query.users) {
        table.append(
            $('<tr>').append(
                $('<td>', {'text': 'From these users:', 'class': 'w35pc'})
            ).append(
                $('<td>', {'text': query.users})
            )
        )
    }

    if (query.date_from) {
        table.append(
            $('<tr>').append(
                $('<td>', {'text': 'From this date:', 'class': 'w35pc'})
            ).append(
                $('<td>', {'text': query.date_from})
            )
        )
    }

    if (query.date_to) {
        table.append(
            $('<tr>').append(
                $('<td>', {'text': 'To this date:', 'class': 'w35pc'})
            ).append(
                $('<td>', {'text': query.date_to})
            )
        )
    }

    table.append(
        $('<tr>').append(
            $('<td>', {'text': 'Search query:', 'class': 'w35pc'})
        ).append(
            $('<td>', {'text': query.search_query})
        )
    );

    return table;
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
                    'class': 'stop-query',
                    'id': query.id,
                    'html': '<i class="fa fa-stop">&nbsp;</i>Stop'
                }).click(lnkStopQueryClickHandler)
            ).append(
                $('<span>', {'html': '&nbsp;'})
            ).append(
                $('<a>', {
                    'href': "#",
                    'class': 'run-query',
                    'id': query.id,
                    'html': '<i class="fa fa-play">&nbsp;</i>Run'
                }).click(lnkRunQueryClickHandler)
            ).append(
                $('<span>', {'html': '&nbsp;'})
            ).append(
                $('<a>', {
                    'href': "#",
                    'class': 'edit-query',
                    'id': query.id,
                    'html': '<i class="fa fa-pencil">&nbsp;</i>Edit'
                })
            ).append(
                $('<span>', {'html': '&nbsp;'})
            ).append(
                $('<a>', {
                    'href': "#",
                    'class': 'delete-query',
                    'id': query.id,
                    'html': '<i class="fa fa-trash">&nbsp;</i>Delete'
                }).click(lnkDeleteQueryClickHandler)
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

function lnkDeleteQueryClickHandler() {
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

function lnkRunQueryClickHandler() {
    var id = $(this).prop('id');
    var request_path = host + '/queries/run/';
    var linkRun = $(this);
    $.post(
        request_path,
        {
            csrfmiddlewaretoken: csrf_token,
            query_id: id
        },
        function (response) {
            if (response.status == 'success') {
                linkRun.hide();
                linkRun.parent().find(".stop-query").show();
            }
        }
    );
}

function lnkStopQueryClickHandler() {
    var id = $(this).prop('id');
    var request_path = host + '/queries/stop/';
    var linkStop = $(this);
    $.post(
        request_path,
        {
            csrfmiddlewaretoken: csrf_token,
            query_id: id
        },
        function (response) {
            if (response.status == 'stopped') {
                linkStop.hide();
                linkStop.parent().find(".run-query").show();
            }
        }
    );
}

$(document).ready(function () {
    csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $('#btn-create-query').click(btnCreateQueryClickHandler);
    getMyQueries();
});