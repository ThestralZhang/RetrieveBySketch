/**
 * Created by ZTR on 25/05/2017.
 */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function displayMsg(msg) {
    if($('#msg-hint').length > 0){
        $('#msg-hint').remove();
    }
    if(msg)
        $('#login-form').before(
            "<div id='msg-hint'>" +
                msg +
            "</div>"
        );
}

function login() {
    console.log('eeeeee')
    var username = $('#usr-nm').val();
    var password = $('#ps-wd').val();

    if(username.length == 0 || username[0] == ' ' || username.split(' ').length > 1){
        displayMsg('Space is not allowed in username.');
        return;
    }
    displayMsg();
    password = md5(password);
    $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:8000/login/',
            data: JSON.stringify({'username': username, 'password': password}),
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                if(data.result == 'success')
                    window.location.href='/home/';
                else
                    displayMsg(data.msg);
            },
            error: function () {
                displayMsg('Oops! Failed to log in.');
            }
    });

}

$(document).ready(function(){
        $('#login-btn').click(function () {
            login();
        });
});


