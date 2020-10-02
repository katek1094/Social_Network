
function gallery_link(auth_user_id) {
    let current_url = window.location.href
    let scrollY = parseInt(window.scrollY)
    console.log('cos sie dzieje')
    $.ajax({
        url: pre_gallery_url,
        type: 'POST',
        data: {
            auth_user_id: auth_user_id,
            previous_url: current_url,
            scrollY: scrollY,
            csrfmiddlewaretoken: csrf_token,
        },
        dataType: 'json',
        success: function () {
        }
    });
}

function likePostButton(post_id, action) {
    $.ajax({
        url: like_url,
        type: 'POST',
        data: {target_id: post_id,
            csrfmiddlewaretoken: csrf_token,
            action: action,
            target_type: 'post'},
        dataType: 'json',
        success: function () {
            if (action === 'like') {
                let like_button_section = document.getElementById(`like-button-${post_id}`)
                like_button_section.innerHTML = `<button class='btn btn-primary' id='unlike-${post_id}'` +
                    ` >unlike</button>`
                document.getElementById(`unlike-${post_id}`).addEventListener('click', function () {
                    likePostButton(post_id, 'unlike')
                })
            }
            if (action === 'unlike') {
                let like_button_section = document.getElementById(`like-button-${post_id}`)
                like_button_section.innerHTML = `<button class='btn btn-secondary' id='like-${post_id}'` +
                    ` >like</button>`
                document.getElementById(`like-${post_id}`).addEventListener('click', function () {
                    likePostButton(post_id, 'like')
                })
            }
        }
    });
}

function commentPostButton(post_id) {
    let comment_field = document.getElementById(`new-comment_content-${post_id}`)
    let text = comment_field.value
    console.log(text)
    if (text !== '') {
        $.ajax({
        url: comment_url,
        type: 'POST',
        data: {post_id: post_id,
            text: text,
            csrfmiddlewaretoken: csrf_token},
        dataType: 'json',
        success: function () {
            comment_field.value = ''
            // TODO: display new comment if success
        }
    });
    }
}







$('.autoresizing').on('input', function () {
            this.style.height = '2em';
            this.style.height = (this.scrollHeight) + 'px';
        });