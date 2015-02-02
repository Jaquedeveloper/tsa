var csrf_token = null;
var host = 'http://' + document.domain + ':8000';
var taskGetResults = null;
var five_seconds = 5000;
var editing = false;
var editId = null;
var runningQueryId = null;

function getMessage(msg, type, id, close_button) {
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

function notify(data) {
    var message = getMessage(data.message, data.status, "5000msNotice", false);
    $("#status-message").empty().append(message);
    message.delay(5000).fadeOut();
}


function btnCreateQueryClickHandler() {
    var request_path = host + "/queries/new/";
    var request_data = {
        csrfmiddlewaretoken: csrf_token,
        id: editId,
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

    if (editing) {
        request_path = host + "/queries/edit/";
        request_data['editing'] = editing;
    }

    if (request_data.title.length == 0) {
        $("#title").addClass('error');
        $('label[for="title"]').addClass('error');
        return false;
    } else {
        $("#title").removeClass('error');
        $('label[for="title"]').removeClass('error');
    }

    if (
        request_data.all_words.length == 0 && request_data.phrase.length == 0 && request_data.any_word.length == 0 &&
        request_data.none_of.length == 0 && request_data.hashtags.length == 0 && request_data.users.length == 0 &&
        request_data.date_from.length == 0 && request_data.date_to.length == 0
    ) {
        alert('At least one field of the query must be filled');
        return false;
    }

    $.post(
        request_path,
        request_data,
        function (data) {
            notify(data);
            if (data.status == 'success') {
                clearNewQueryForm();
                $('#is_public').val("");
                var qw = $("#queries");
                qw.find($('h6')).remove();

                if (data.edited) {
                    editing = false;
                    $("#btn-create-query").text("Create");
                    $("#q" + editId).remove();
                    $("a[href='#my_queries']").click();
                }
                renderQuery(data['query'], qw, false);
            }
        }
    );
}


function lnkEditQueryClickHandler() {
    var id = $(this).prop('id');
    editId = id;
    var request_path = host + '/queries/get/';
    $.post(
        request_path,
        {
            csrfmiddlewaretoken: csrf_token,
            query_id: id
        },
        function (response) {
            notify(response);
            if (response.status == 'success') {
                fillNewQueryForm(response.query);
                $("a[href='#new_query']").click();
                editing = true;
                $("#btn-create-query").text("Edit");
            }
        }
    );

    return false;
}


function lnkDeleteQueryClickHandler() {
    if (!confirm('Are you sure?')) return false;
    var request_path = host + '/queries/delete/';
    var id = $(this).prop('id');
    $.post(
        request_path,
        {
            csrfmiddlewaretoken: csrf_token,
            query_id: id
        },
        function (response) {
            notify(response);
            if (response.status == 'success') {
                runningQueryId = null;
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
            notify(response);
            if (response.status == 'success') {
                runningQueryId = id;
                taskGetResults = createTask(getQueryResults, five_seconds, runningQueryId);
                $("#waiting").show();
                $("#nq").hide();
                linkRun.hide();
                linkRun.parent().find(".stop-query").show();
                $("a[href='#my_dashboard']").click();
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
            notify(response);
            if (response.status == 'success') {
                clearInterval(taskGetResults);
                linkStop.hide();
                linkStop.parent().find(".run-query").show();
            }
        }
    );
}

function getMyQueries() {
    var request_path = host + '/queries/my/';
    $.post(
        request_path,
        {csrfmiddlewaretoken: csrf_token},
        function (data) {
            if (data.hasOwnProperty('queries')) {
                var div = $("#queries");
                renderQueries(data['queries'], div);
            }
            if (data.running_query_id) {
                var id = data.running_query_id;
                // very strange, this way works, but $("a.run-query#" + id) not
                $("a.run-query[id=" + id + "]").hide();
                $("a.stop-query[id=" + id + "]").show();
                runningQueryId = id;
                if (!taskGetResults)
                    taskGetResults = createTask(getQueryResults, five_seconds, id);
                $("#tweets").html('<div id="waiting" style="display: none"><img src="/static/images/ajax-loader.gif" alt="loading" /><h6>Waiting for tweets, one moment please</h6></div>');
            }
        }
    );
}

function getGroupQueries() {
    var request_path = host + '/queries/group/';
    $.post(
        request_path,
        {csrfmiddlewaretoken: csrf_token},
        function (data) {
            if (data.hasOwnProperty('queries')) {
                var div = $("#g_queries");
                renderQueries(data['queries'], div);
            }
            if (data.running_query_id) {
                var id = data.running_query_id;
                runningQueryId = id;
                // very strange, this way works, but $("a.run-query#" + id) not
                $("a.run-query[id=" + id + "]").hide();
                $("a.stop-query#" + id).show();
                if (!taskGetResults)
                    taskGetResults = createTask(getQueryResults, five_seconds, id);
                $("#tweets").html('<div id="waiting" style="display: none"><img src="/static/images/ajax-loader.gif" alt="loading" /><h6>Waiting for tweets, one moment please</h6></div>');
            }
        }
    );
}

function renderQueries(queries, where) {
    if (queries == null || queries.length == 0) {
        where.append($('<h6>', {'text': 'There are no queries yet'}));
        return;
    }

    queries.forEach(function (query) {
        renderQuery(query, where, true);
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
                    'class': 'analyse-query',
                    'id': query.id,
                    'html': '<i class="fa fa-bar-chart">&nbsp;</i>Analyse (offline)'
                }).click(lnkAnalyseQueryClickHandler)
            ).append(
                $('<span>', {'html': '&nbsp;'})
            ).append(
                $('<a>', {
                    'href': "#",
                    'class': 'stop-query',
                    'id': query.id,
                    'html': '<i class="fa fa-stop">&nbsp;</i>Stop'
                }).click(lnkStopQueryClickHandler).hide()
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
                }).click(lnkEditQueryClickHandler)
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


function clearNewQueryForm() {
    $('#title').val("");
    $('#all_words').val("");
    $('#phrase').val("");
    $('#any_word').val("");
    $("#none_of").val("");
    $("#hashtags").val("");
    $("#users").val("");
    $("#df").val("");
    $("#dt").val("");
}

function createTask(func, interval, data) {
    return setInterval(func, interval, data);
}

function createFreqWordsTable(words) {
    var FR = 0;
    var TEXT = 1;
    var table = $('<table>');

    words.forEach(function (word) {
        table.append(
            $('<tr>').append(
                $('<td>', {
                    'text': word[TEXT],
                    'class': 'w35pc'
                })
            ).append(
                $('<td>', {
                    'text': word[FR]
                })
            )
        );
    });

    return table;
}

function getHashtagsString(hashtags) {
    var str = '';
    var TEXT = 1;

    hashtags.forEach(function (item) {
        str += '#' + item[TEXT] + '   ';
    });

    return str;
}

function getUsersString(users) {
    var str = '';

    users.forEach(function (user) {
        str += '@' + user + '     ';
    });

    return str;
}
function displayStatistics(analysis) {
    var div = $('#st');
    div.empty();

    var table = $('<table>');

    table.append(
        $('<tr>').append(
            $('<th>', {
                'text': 'Keywords:',
                'class': 'top-text'
            })
        ).append(
            $('<td>', {
                'text': analysis.keywords
            })
        )
    ).append(
        $('<tr>').append(
            $('<th>', {
                'text': 'Hashtags:',
                'class': 'top-text'
            })
        ).append(
            $('<td>', {
                'text': getHashtagsString(analysis.hashtags)
            })
        )
    ).append(
        $('<tr>').append(
            $('<th>', {
                'text': 'Users:',
                'class': 'top-text'
            })
        ).append(
            $('<td>', {
                'text': getUsersString(analysis.users)
            })
        )
    ).append(
        $('<tr>').append(
            $('<th>', {
                'text': 'Frequent words:',
                'class': 'top-text'
            })
        ).append(
            $('<td>', {
                'html': createFreqWordsTable(analysis.word_counts)
            })
        )
    );

    div.append(table);
}

function getQueryResults(id) {
    var request_path = host + '/queries/results/';
    $.post(
        request_path,
        {
            csrfmiddlewaretoken: csrf_token,
            query_id: id
        },
        function (response) {
            if (response.status == 'success') {
                renderTweets(response.tweets);
                displayStatistics(response.analysis);
                runningQueryId = id;
            } else {
                notify(response)
            }
        }
    );
}

function renderTweet(tweet, where) {
    var tweetDiv = $('<div>', {
        'class': 'tweet'
    });

    tweetDiv.append(
        $('<div>', {
            'class': 'tweet-title'
        }).append(
            $('<div>', {
                'class': 'tweet-posted-by',
                'text': 'Posted by: '
            }).append($('<span>', {'class': 'tweet-owner', 'text': tweet.user}))
        ).append(
            $('<div>', {
                'class': 'tweet-date',
                'text': 'Since: '
            }).append($('<span>', {'text': tweet.date}))
        )
    ).append(
        $('<div>', {
            'class': 'tweet-body',
            'text': tweet.text
        }).append($('<div>', {
            'class': 'tweet-polarity',
            'html': getTweetPolarityView(tweet.polarity)
        }))
    );

    where.append(tweetDiv);
}

function getTweetPolarityView(polarity) {
    var span = $('<span>');

    if (polarity == 0.0) {
        span.append($('<i>', {
            'class': 'fa fa-circle-thin pn',
            'html': '&nbsp;' + polarity
        }));
    } else if (polarity < 0.0) {
        span.append($('<i>', {
            'class': 'fa fa-frown-o png',
            'html': '&nbsp;' + polarity
        }));
    } else {
        span.append($('<i>', {
            'class': 'fa fa-smile-o pp',
            'html': '&nbsp;' + polarity
        }));
    }

    return span;
}

function renderTweets(tweets) {
    var div = $("#tweets");
    div.empty();
    tweets.forEach(function (tweet) {
        renderTweet(tweet, div);
    });
}


function fillNewQueryForm(query) {
    $('#title').val(query.title);
    $('#all_words').val(query.all_words);
    $('#phrase').val(query.phrase);
    $('#any_word').val(query.any_word);
    $("#none_of").val(query.none_of);
    $("#hashtags").val(query.hashtags);
    $("#users").val(query.users);
    $("#df").val(query.date_from);
    $("#dt").val(query.date_to);
}


function lnkAnalyseQueryClickHandler() {
    var id = $(this).prop('id');
    getQueryResults(id);
    $("a[href='#my_dashboard']").click();
}

function lnkRemoveUserFromGroupClickHandler() {
    if (!confirm('Are you sure?')) return;
    var id = $(this).prop('id');
    var request_path = host + '/accounts/group/remove/';
    var linkRemove = $(this);
    $.post(
        request_path,
        {
            csrfmiddlewaretoken: csrf_token,
            user_id: id
        },
        function (response) {
            notify(response);
            if (response.status == 'success') {
                getGroupQueries();
                linkRemove.parent().parent().remove();
            }
        }
    );
    return false;
}

function btnFilterClickHandler() {
    if (!runningQueryId) return false;
    var ftf = $("#filter-text");
    ftf.removeClass("error");
    var filterText = ftf.val();

    if (!filterText) {
        ftf.addClass("error");
        return false;
    }

    window.location.href = host + '/queries/filter/' + runningQueryId + "/" + filterText + "/";
    return false;
}

$(document).ready(function () {
    csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
});