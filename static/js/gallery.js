let right = 0;
let left = 0;

document.onkeydown = checkKey;
function checkKey(e) {
    if (e.keyCode === 37) {
        // left arrow
        if (left) {
            document.getElementById('left_button').click()
        }
    }
    else if (e.keyCode === 39) {
        // right arrow
        if (right) {
            document.getElementById('right_button').click()
        }
    }
    else if (e.keyCode === 27) {
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

function likeImageButton(image_id, action) {
    $.ajax({
        url: like_url,
        type: 'POST',
        data: {target_id: image_id,
            csrfmiddlewaretoken: csrf_token,
            action: action,
            target_type: 'image'},
        dataType: 'json',
        success: function () {
            if (action === 'like') {
                let like_button_section = document.getElementById(`like-button-${image_id}`)
                like_button_section.innerHTML = `<button class='btn btn-primary' id='unlike-${image_id}'` +
                    ` >unlike</button>`
                document.getElementById(`unlike-${image_id}`).addEventListener('click', function () {
                    likeImageButton(image_id, 'unlike')
                })
            }
            if (action === 'unlike') {
                let like_button_section = document.getElementById(`like-button-${image_id}`)
                like_button_section.innerHTML = `<button class='btn btn-secondary' id='like-${image_id}'` +
                    ` >like</button>`
                document.getElementById(`like-${image_id}`).addEventListener('click', function () {
                    likeImageButton(image_id, 'like')
                })
            }
        }
    });
}
