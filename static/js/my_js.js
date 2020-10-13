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
    let paragraph = document.getElementById(`likes_counter-${type}-${id}`)
    if (paragraph) {
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
                paragraph.remove()
            }}}
    else {
        document.getElementById(`likes_counter_section_${type}-${id}`).innerHTML = `<p id='likes_counter-${type}-${id}' class="likes_counter">1 people like this</p>`
    }
}

function likeButton(type, id) {
    // types: post, comment, image, actions: like, unlike
    let like_button = document.getElementById(`like_button-${type}-${id}`)
    let action
    if (like_button.classList.contains('like')) {
        action = 'like'
    }
    if (like_button.classList.contains('unlike')) {
        action = 'unlike'
    }
    $.ajax({
        url: like_url,
        type: 'POST',
        data: {target_id: id,
            csrfmiddlewaretoken: csrf_token,
            action: action,
            target_type: type},
        dataType: 'json',
        success: function () {
            like_button.classList.toggle('like')
            like_button.classList.toggle('unlike')
            likesCounter(action, type, id)
            if (action === 'like') {
                like_button.innerText = 'unlike'
            }
            if (action === 'unlike') {
                like_button.innerText = 'like'
            }
        }});}

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
            let comments_section = document.getElementById(`comments_list-${type}-${id}`);
            comments_section.insertAdjacentHTML('beforeend', response.new_comment_html)
        }
    });}}

function autoresizing() {
    $('.autoresizing').on('input', function () {
        let el = this
        let padding = parseInt(getComputedStyle(el).padding.replace('px', ''))
        let font_size = parseInt(getComputedStyle(el).fontSize.replace('px', ''))
        // let basic_height = (font_size + (2 * padding)).toString() + 'px'
        // this.style.height = basic_height
        // let new_height = this.scrollHeight - (padding * 2)
        // this.style.height = new_height + 'px';
        // 8 - 1
        // 12 - 2
        // 16 - 3
        // 24 - 4
        // 32 - 5
        let x = 1
        if (font_size > 28) {x = 5}
        else {
            if (font_size > 20) {x = 4}
            else {
                if (font_size > 14) {x = 3}
                else {
                    if (font_size > 10) {x = 2}
                }}}
        this.style.height = '1em';
        this.style.height = this.scrollHeight - x - 2 * padding + 'px'
    });}


function friendshipButton(auth_profile_user_id, visited_profile_user_id) {
    let button = document.getElementsByClassName('friendship_button')[0]
    let action = button.innerText
    $.ajax({
        url: friendship_button_url,
        type: 'POST',
        data: {
            auth_profile_user_id: auth_profile_user_id,
            action: action,
            visited_profile_user_id: visited_profile_user_id,
            csrfmiddlewaretoken: csrf_token,
        },
        dataType: 'json',
        success: function (response) {
            button.innerText = response.new_action
        }
    });}


$(document).ready(autoresizing())