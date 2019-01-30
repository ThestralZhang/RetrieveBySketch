/**
 * Created by ZTR on 17/05/2017.
 */
var clmIdx = 0;
var detailed;

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

function equipModal() {
    $('#detail-modal .info a').click(function () {
        $('.modal-overlay').css('visibility', 'hidden');
        $('body').css('overflow','auto');
    });
}

function displayImgs(imgs, owners) {
    var num = 5;
    var idx = 0;
    for(var i = 0; i < imgs.length; i++){
        idx = (i+clmIdx)%num;
        // if(idx == 0) idx = 5;
        $('.column:eq('+idx+')').append(
            '<div class="frame">' +
                '<div class="box">' +
                    '<span><img src="/media/' + imgs[i] + '"></span>' +
                '</div>' +
                '<div class="info">' +
                    '<a>by ' + owners[i] + '</a>' +
                    '<input type="checkbox" checked="checked">' +
                '</div>' +
            '</div>'
        );
    }
    $('.frame img').click(function () {
        console.log('detail');
        $('.modal-overlay').css('visibility', 'visible');
        $('#detail-modal img').attr('src', $(this).attr('src'));
        detailed = $(this).parent().parent().next().find('input');
        if(detailed.attr('checked'))
            $('#detail-modal .info input').attr('checked', 'checked');
        else
            $('#detail-modal .info input').attr('checked', false);
        $('body').css('overflow','hidden');
        $('body').css('overflow','hidden');
    });
    $('.info input').click(function () {
        var act = 'unlike';
        var src = $(this).parent().prev().find('img').attr('src');
        if($(this).attr('checked')=='checked')
            act = 'like';
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:8000/like_img/',
            data: {'act': act, 'src': src},
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                console.log(act + ' img')
            },
            error: function () {
                console.log('error');
            }
        });
        if($(this).parent().parent().attr('id') == 'detail-modal'){
            if(act == 'like'){
                detailed.attr('checked','checked');
            }else{
                detailed.attr('checked',false);
            }
        }
    });
    clmIdx = idx;
}

function loadPage() {
    $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:8000/load_likes/',
        data: {'test': 1},
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            console.log(data.imgs)
            console.log(data.owners)
            $('.column').html('');
            clmIdx = 0;
            displayImgs(data.imgs, data.owners);
        },
        error: function () {
            console.log('error');
        }
    });
}

$(document).ready(function(){
    loadPage();
    equipModal();
});
