/**
 * Created by ZTR on 07/06/2017.
 */
/**
 * Created by ZTR on 17/05/2017.
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

function equipModal() {
    $('#detail-modal .info a').click(function () {
        $('.modal-overlay').css('visibility', 'hidden');
        $('body').css('overflow','auto');
    });
}

function displayImgs(imgs) {  // imgs
    var cur_ds =  '';
    var cn = 0;
    for(var i = 0; i < imgs.length; i++){
        ds = imgs[i][1];
        if(ds != cur_ds){
            $('body').append(
                '<div class="panel">' +
                    '<div class="column"></div>' +
                    '<div class="column"></div>' +
                '</div>'
            );
            cn = 0;
            cur_ds = ds;
        }
        $('.panel').last().find('.column:nth-child('+(cn%2+1)+')').append(
            '<div class="up-item">' +
                '<div class="preview">' +
                    '<span><img src="/media/' + imgs[i][0] + '"></span>' +
                '</div>' +
                '<p>' + ds + '</p>' +
            '</div>'
        );
        cn++;
    }
    $('.up-item').click(function () {
        console.log('detail');
        $('.modal-overlay').css('visibility', 'visible');
        $('#detail-modal img').attr('src', $(this).find('img').attr('src'));
        $('body').css('overflow','hidden');
        $('body').css('overflow','hidden');
    });
}

function loadPage() {
    $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:8000/load_ups/',
        data: {'test': 1},
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            console.log(data.imgs)
            displayImgs(data.imgs);
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
