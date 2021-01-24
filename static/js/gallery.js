document.onkeydown = checkKey;

function checkKey(e) {
    if (e.keyCode === 37) {
        // left arrow
        if (left) {
            document.getElementsByClassName('gallery_button left')[0].click()
        }
    } else if (e.keyCode === 39) {
        // right arrow
        if (right) {
            document.getElementsByClassName('gallery_button right')[0].click()
        }
    } else if (e.keyCode === 27) {
        // escape
        document.getElementById('gallery_exit_button').click()
    }
}

function gallery_exit(auth_user_id) {
    $.ajax({
        url: pre_gallery_url,
        type: 'GET',
        data: {
            auth_user_id: auth_user_id,
        },
        dataType: 'json',
        success: function (response) {
            window.location.href = response.url
            // {#window.scrollTo(0, response.scrollY)#}
            // {#tutaj mozna kiedys dodac opcje wracanie w to samo miejsce na stronie#}
        }
    });
}
