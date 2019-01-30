/**
 * Created by ZTR on 17/05/2017.
 */
var drawFlag = 1;   // draw: 1   erase: 0
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
    var s1 = document.getElementById('open-btn');
    var s2 = document.getElementById('close-btn');
    var s3 = document.getElementById('up-btn');
    var s4 = document.getElementById('ccl-btn');

    s1.addEventListener('click', switchModal1);
    s2.addEventListener('click', switchModal1);
    s3.addEventListener('click', switchModal2);
    s4.addEventListener('click', switchModal2);

    $('#detail-modal .info a').click(function () {
        $('.modal-overlay').css('visibility', 'hidden');
        $('body').css('overflow','auto');
    });
}

function switchModal1() {
    var e1 = document.getElementById('modal-overlay1');
    // e1.style.visibility = (e1.style.visibility == 'visible') ? "hidden" : "visible";
    if(e1.style.visibility == 'visible'){
        e1.style.visibility = 'hidden';
        $('#larger-btn').css('visibility', 'hidden');
        $('#smaller-btn').css('visibility', 'hidden');
        $('body').css('overflow','auto');
        console.log('11111');
    }else{
        e1.style.visibility = 'visible';
        if(drawFlag == 0){
            $('#larger-btn').css('visibility', 'visible');
            $('#smaller-btn').css('visibility', 'visible');
        }
        $('body').css('overflow','hidden');
        console.log('22222');

    }
}

function switchModal2() {
    var e1 = document.getElementById('modal-overlay2');
    // e1.style.visibility = (e1.style.visibility == 'visible') ? "hidden" : "visible";
    if(e1.style.visibility == 'visible'){
        e1.style.visibility = 'hidden';
        $('body').css('overflow','auto');
    }else{
        e1.style.visibility = 'visible';
        $('body').css('overflow','hidden');
    }
}

function enableDrawing() {
    var cvs = document.getElementById("draw-pad");
    var cxt = cvs.getContext('2d');
    var isPressed = false;          // is mouse pressed
    var isFirstDrop = false;   // first drop on each stroke

    $('#draw-btn').click(function () {
        if(drawFlag == 1)
            return;
        $('#draw-btn img').attr('src', '');
        $('#erase-btn img').attr('src', '/static/image/u_eraser.png');
        $('#larger-btn').css('visibility', 'hidden');
        $('#smaller-btn').css('visibility', 'hidden');
        $('#draw-pad').css('cursor','url("/static/image/pen_cursor.png"), default');
        drawFlag = 1;
    });

    $('#draw-btn img').hover(function () {
        $(this).attr('src', '/static/image/a_pen.png');
    }, function () {
        if(drawFlag == 1)
            $(this).attr('src', '/static/image/pen.png');
        else
            $(this).attr('src', '/static/image/u_pen.png');
    });

    $('#erase-btn').click(function () {
        if(drawFlag == 0)
            return;
        $('#draw-btn img').attr('src', '/static/image/u_pen.png');
        $('#erase-btn img').attr('src', '/static/image/eraser.png');
        $('#larger-btn').css('visibility', 'visible');
        $('#smaller-btn').css('visibility', 'visible');
        $('#draw-pad').css('cursor','none');
        drawFlag = 0;
    });

    $('#erase-btn img').hover(function () {
        $(this).attr('src', '/static/image/a_eraser.png');
    }, function () {
        if(drawFlag == 0)
            $(this).attr('src', '/static/image/eraser.png');
        else
            $(this).attr('src', '/static/image/u_eraser.png');
    });

    cvs.addEventListener('mousedown', function () {
        isPressed = true;
        isFirstDrop = true;
    }, false);
    cvs.addEventListener('mouseup', function () {
        isPressed = false;
    }, false);
    cvs.addEventListener('mouseenter', function () {
        if(drawFlag == 0)
            $('#eraser').css('visibility', 'visible');
    }, false);
    cvs.addEventListener('mouseout', function () {
        isPressed = false;
        $('#eraser').css('visibility', 'hidden');
    }, false);


    // 1. onChange
    // 2. onMouseEnter then check the value

    // when pen, change cursor, drawable
    // when erase, change cursor, erasable, show two more buttons, let the corresponding image follow the cursor


    cvs.addEventListener('mousemove', function (e) {
        if(drawFlag == 1 && isPressed){
            if(!isFirstDrop)
                cxt.lineTo(e.offsetX, e.offsetY);
            else
                isFirstDrop = false;
            cxt.stroke();
            cxt.moveTo(e.offsetX, e.offsetY);
        }else{
            $('#eraser').css({'top':e.clientY, 'left':e.clientX});
            if(isPressed){
                var size = parseInt($('#eraser').css('width'));
                cxt.clearRect(e.offsetX, e.offsetY, size, size);
                cxt.beginPath();
            }
        }
    }, false);

    var canLarger = 1;
    var canSmaller = 1;
    $('#larger-btn').click(function () {
        if(canLarger == 0)
            return;
        var size = parseInt($('#eraser').css('width'));
        // 9 15 21 27 33 39 45 51
        canSmaller = 1;
        $('#smaller-btn img').attr('src', '/static/image/smaller.png');
        size += 8;
        $('#eraser').css({'width': size + 'px', 'height': size + 'px'});
        if(size == 81){
            canLarger = 0;
            $('#larger-btn img').attr('src', '/static/image/u_larger.png');
        }
    });

    $('#larger-btn img').hover(function () {
        if(canLarger == 1)
            $(this).attr('src', '/static/image/a_larger.png');
    }, function () {
        if(canLarger == 1)
            $(this).attr('src', '/static/image/larger.png');
    });

    $('#smaller-btn').click(function () {
        if(canSmaller == 0)
            return;
        var size = parseInt($('#eraser').css('width'));
        // 9 15 21 27 33 39 45 51
        // 9 17 25 33 41 49 57 65 73 81
        canLarger = 1;
        $('#larger-btn img').attr('src', '/static/image/larger.png');
        size -= 8;
        $('#eraser').css({'width': size + 'px', 'height': size + 'px'});
        if(size == 9){
            canSmaller = 0;
            $('#smaller-btn img').attr('src', '/static/image/u_smaller.png');
        }
    });

    $('#smaller-btn img').hover(function () {
        if(canSmaller == 1)
            $(this).attr('src', '/static/image/a_smaller.png');
    }, function () {
        if(canSmaller == 1)
            $(this).attr('src', '/static/image/smaller.png');
    });

    $('#clear-btn').click(function () {
        cxt.clearRect(0, 0, cvs.width, cvs.height);
        cxt.beginPath();
    });

    $('#clear-btn img').hover(function () {
        $(this).attr('src', '/static/image/a_clear.png');
    }, function () {
        $(this).attr('src', '/static/image/clear.png');
    });
}

function passSketchData() {
    var cvs = document.getElementById("draw-pad");
    var cxt = cvs.getContext('2d');
    $('#retrieve-btn').click(function () {
        var w = cvs.width;
        var h = cvs.height;
        var pxData = cxt.getImageData(0, 0, w, h).data;
        var ones = [];
        var i = 0;
        while(4*i < pxData.length){
            if(pxData[4*i+3] >= 200)
                ones.push(i);
            i++;
        }
        if(ones.length < 300){
            console.log("need more pixels");
            return;
        }
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:8000/load_imgs/',
            data: JSON.stringify({'width': w, 'height': h, 'ones':ones}),
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                console.log('get images');
                switchModal1();
                $('.column').html('');
                clmIdx = 0;
                displayImgs(data.imgs, data.likes, data.owners);
                setTimeout(load_candice(), 10000);
            },
            error: function () {
                console.log('rt error');
            }
        });
    });

    // $('#retrieve-btn').click(function () {
    //
    // })
    //
    // $('#retrieve-btn').click(function () {
    //
    // });
}

function load_candice() {
    $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:8000/load_1st_candice/',
        data: {'test': 1},
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            $('#candidates').html('');
            displayCandice(data.candice);
        },
        error: function () {
            console.log('error');
        }
    });
    $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:8000/load_candice/',
        data: {'test': 1},
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            console.log('load candice done')
        },
        error: function () {
            console.log('error');
        }
    });
}


function displayImgs(imgs, likes, owners) {
    var num = 5;
    var idx = 0;
    for(var i = 0; i < imgs.length; i++){
        idx = (i+clmIdx)%num;
        if(likes[i] == 1)
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
        else
            $('.column:eq('+idx+')').append(
                '<div class="frame">' +
                    '<div class="box">' +
                        '<span><img src="/media/' + imgs[i] + '"></span>' +
                    '</div>' +
                    '<div class="info">' +
                        '<a>by ' + owners[i] + '</a>' +
                        '<input type="checkbox">' +
                    '</div>' +
                '</div>'
            );
    }
    $('.frame img').click(function () {
        console.log('detail');
        $('#modal-overlay3').css('visibility', 'visible');
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
    $('#no-more').css('display', 'none');
    $('#ld-mr-btn').css('display','block');
}

function displayCandice(candice) {
    if(candice.length == 0)
        return;

    $('#candidates').html('<h4>You may want to search:</h4>');
    for(var i = 0; i < candice.length; i++){
        $('#candidates').append('<p class="candi-card">' +
            candice[i] +
            '</p>');
    }
    $('#candidates').append('<button id="chg-cd-btn">change...</button>');

    $('.candi-card').click(function () {
        var isChosen = $(this).hasClass('chosen-candi');
        $('.candi-card').removeClass('chosen-candi');
        if(isChosen){
            $.ajax({
                type: 'GET',
                url: 'http://127.0.0.1:8000/unselect_candi/',
                data: {'test': 1},
                dataType: 'json',
                contentType: 'application/json',
                success: function (data) {
                    $('.column').html('');
                    clmIdx = 0;
                    displayImgs(data.imgs, data.likes, data.owners);
                    $('#no-more').css('display', 'none');
                    $('#ld-mr-btn').css('display','block');
                },
                error: function () {
                    console.log('error');
                }
            });
            return;
        }
        $(this).addClass('chosen-candi');
        candi = $(this).text();
        console.log(candi)
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:8000/select_candi/',
            data: {'candi': candi},
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                $('.column').html('');
                clmIdx = 0;
                displayImgs(data.imgs, data.likes, data.owners);
                $('#no-more').css('display', 'none');
                $('#ld-mr-btn').css('display','none');
            },
            error: function () {
                console.log('error');
            }
        });
        console.log('candi')
    });

    $('#chg-cd-btn').click(function () {
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:8000/change_candice/',
            data: {'test': 1},
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                $('#candidates').html('');
                displayCandice(data.candice);
            },
            error: function () {
                console.log('error');
            }
        });
    });
}

function loadMore() {
    $('#ld-mr-btn').click(function () {
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:8000/load_more/',
            data: {'test': 1},
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                if(data.imgs.length == 0){
                    $('#no-more').css('display', 'block');
                    $('#ld-mr-btn').css('display','none');
                }else{
                    displayImgs(data.imgs, data.likes, data.owners);
                }
            },
            error: function () {
                console.log('error');
            }
        });
    });
}

function displayMsg(msg) {
    if($('#msg-hint').length > 0){
        $('#msg-hint').remove();
    }
    if(msg)
        $('#upload-modal').before(
            "<div id='msg-hint'>" +
                msg +
            "</div>"
        );
}

function submitImg() {
    var fileInput = document.getElementById('up-img');
    var filename = document.getElementById('file-name');
    var preview = document.getElementById('preview');
    var msg = '';

    fileInput.addEventListener('change', function () {
        if (!fileInput.value) {
            preview.innerHTML = '<span>The preview will be shown here.</span>';
            filename.innerHTML = 'file name';
            msg = 'no chosen file';
            console.log('no');
            return;
        }
        preview.style.backgroundImage = '<span></span>';
        var file = fileInput.files[0];
        filename.innerHTML = file.name;

        if (file.type !== 'image/jpeg' && file.type !== 'image/png' && file.type !== 'image/jpg') {
            msg = 'not valid type';
            return;
        }
        var reader = new FileReader();
        reader.onload = function(e) {
            var data = e.target.result;
            preview.innerHTML = '<span><img src="'+data+'"></span>';
            // preview.style.backgroundImage = 'url(' + data + ')';
        };
        // 以DataURL的形式读取文件:
        reader.readAsDataURL(file);
    });

    $('#sub-btn').click(function () {
        var fileObj = $("#up-img")[0].files[0];
        var form = new FormData();
        form.append('img', fileObj);
        form.append('tag1', $('#tag1').val());
        form.append('tag2', $('#tag2').val());
        form.append('tag3', $('#tag3').val());
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/upload_imgs/",
            data: form,
            processData: false,
            contentType: false,
            success: function (arg) {
                console.log(arg);
            },
            error: function () {
                console.log('error');
            }
        })
    });
}

function loadPage() {
    $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:8000/load_home/',
        data: {'test': 1},
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            console.log(data.imgs);
            displayImgs(data.imgs, data.likes, data.owners);
            $('#no-more').css('display', 'none');
            $('#ld-mr-btn').css('display','none');
        },
        error: function () {
            console.log('error');
        }
    });

}

$(document).ready(function(){
        loadPage();
        equipModal();
        enableDrawing();
        passSketchData();
        submitImg();
        loadMore();
    }
);
