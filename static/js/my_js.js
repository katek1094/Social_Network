


function gallery_link(auth_user_id) {
    let current_url = window.location.href
    let scrollY = parseInt(window.scrollY)
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

function likesCounter(action, type, id) {
    let likes_counter_section = document.getElementById(`likes_counter-${type}-${id}`)
    if (likes_counter_section.children[0]) {
        let paragraph = likes_counter_section.children[0]
        let text = paragraph.textContent
        let tab = (text.split(' '))
        let likes = tab[0]
        if (action === 'like') {
            tab[0] = String(Number(tab[0]) + 1)
            text = tab.join(' ')
            paragraph.innerHTML = text
        }
        if (action === 'unlike') {
            if (likes !== '1') {
                tab[0] = String(Number(tab[0]) - 1)
                text = tab.join(' ')
                paragraph.innerHTML = text
            }
            else {
                likes_counter_section.removeChild(paragraph)
            }}}
    else {
        likes_counter_section.innerHTML = '<p>1 people like this</p>'
    }
}

function likeButton(type, id, action) {
    // types: post, comment, image
    $.ajax({
        url: like_url,
        type: 'POST',
        data: {target_id: id,
            csrfmiddlewaretoken: csrf_token,
            action: action,
            target_type: type},
        dataType: 'json',
        success: function () {
            if (action === 'like') {
                let like_button_section = document.getElementById(`like-button-${type}-${id}`)
                like_button_section.innerHTML = `<button class='btn btn-primary' id='unlike-${type}-${id}'` +
                    ` >unlike</button>`
                document.getElementById(`unlike-${type}-${id}`).addEventListener('click', function () {
                    likeButton(type, id, 'unlike')
                })
                likesCounter(action, type, id)
            }
            if (action === 'unlike') {
                let like_button_section = document.getElementById(`like-button-${type}-${id}`)
                like_button_section.innerHTML = `<button class='btn btn-secondary' id='like-${type}-${id}'` +
                    ` >like</button>`
                document.getElementById(`like-${type}-${id}`).addEventListener('click', function () {
                    likeButton(type, id, 'like')
                })
                likesCounter(action, type, id)
            }
        }
    });
}

function commentButton(type, id) {
    // types: post, image
    let comment_field = document.getElementById(`new-comment_content-${type}-${id}`)
    let text = comment_field.value
    console.log(text)
    if (text !== '') {
        $.ajax({
        url: comment_url,
        type: 'POST',
        data: {type: type,
            id: id,
            text: text,
            csrfmiddlewaretoken: csrf_token},
        dataType: 'json',
        success: function (response) {
            comment_field.value = ''
            comments_section = document.getElementById(`comments_list-${type}-${id}`)
            comments_section.insertAdjacentHTML('beforeend', response.new_comment_html)
        }
    });
    }
}


$(document).ready(function(){ /* ... */
$('.autoresizing').on('input', function () {
            this.style.height = '2em';
            this.style.height = (this.scrollHeight) + 'px';
        });});



