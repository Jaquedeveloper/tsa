var csrf_token = null;
var host = 'http://' + document.domain + ':8000';
var queryHtmlTemplate = '<div><span><i class="fa {public} small-font" title="Public query">&nbsp;</i>{title}</span><div class="query-controls"><a href="#">Edit</a> <a href="#">Delete</a></div></div><div class="query-body"><div>{body}</div><div class="query-date">Added: {date}</div></div>';

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
        renderQuery(query, div);
    });
}

function renderQuery(query, container) {
    var div = $('<div>', {
        "class": "query"
    });
    var html = queryHtmlTemplate
        .replace('{title}', query.title)
        .replace('{body}', query.body)
        .replace('{date}', query.date);

    var access = '';
    if (query.is_public) {
        access = 'fa-users';
    } else {
        access = 'fa-lock';
    }

    html = html.replace('{public}', access);
    div.html(html);
    container.append(div);
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
            }
        }
    );
}

$(document).ready(function () {
    csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $('#btn-create-query').click(btnCreateQueryClickHandler);


    getMyQueries();
});