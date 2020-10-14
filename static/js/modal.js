function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }}}
    return cookieValue;
}

let csrftoken = getCookie('csrftoken');


function delete_something(type, id) {
    $.ajax({
        url: delete_url.replace('type', type).replace('2137', id),
        type: 'DELETE',
        data: {
            type: type,
            id: id,
        },
        dataType: 'json',
        beforeSend: xhr => {xhr.setRequestHeader("X-CSRFToken", csrftoken);},
        success: function (response) {
            if (type === 'comment') {document.getElementById(`${type}-${id}`).remove()}
            else if (type === 'post') {document.getElementById(`${type}-${id}`).parentNode.remove()}
            else if (type === 'image') {
            //    TODO: do something after deleting a image
            }
        }
    });
}

function edit_something(type, id, new_text) {
    $.ajax({
        url: edit_url,
        type: "POST",
        data: {
            type: type,
            id: id,
            new_text: new_text,
            csrfmiddlewaretoken: csrf_token,
        },
        dataType: 'json',
        success: function (response) {
            document.getElementById(`text-${type}-${id}`).innerText = new_text
        }
    });
}


function openModal(type, where, content, title) {
    let modal = `<div id="modal">
                        <div class="modal-box">
                            <div class="modal-header">
                                <p class="modal-title">${title}</p>
                                <span id="modal-close">&times;</span>
                            </div>
                            <div class="modal-content">
                                ${content}
                            </div></div></div>`
    where.insertAdjacentHTML('afterend', modal)
    modal = document.getElementById('modal')
    modal.style.setProperty('display', 'flex')
    document.body.style.overflow = 'hidden'
    document.getElementById('modal-close').onclick = closeModal
    window.onclick = function(event) {
        if (event.target === document.getElementById('modal')) {
            closeModal()
        }}
}


function closeModal () {
    document.getElementById('modal').remove()
    document.body.style.overflow = 'initial'
    document.getElementsByClassName('popover')[0].remove()
}


function deleteButton(el, type, id) {
    let title = `Delete ${type}`
    let content = `<p>are you sure you want to delete this ${type}?</p>
                                <div class="modal-buttons">
                                    <button class="modal-button cancel">cancel</button>
                                    <button class="modal-button delete">delete</button>
                                </div>`
    openModal(type, el.parentNode, content, title)
    document.getElementsByClassName('modal-button')[0].onclick = closeModal
    document.getElementsByClassName('modal-button')[1].onclick = () => {
        delete_something(type, id)
        closeModal()
    }
}

function editButton(el, type, id) {
    let text = document.getElementById(`text-${type}-${id}`).textContent
    let title = `Edit ${type}`
    let content = `<textarea id="textarea-edit" class="autoresizing edit_textarea"></textarea>
                        <div class="modal-buttons">
                            <button class="modal-button cancel">cancel</button>
                            <button class="modal-button confirm">confirm</button>
                        </div>`
    openModal(type, el.parentNode, content, title)
    autoresizing()
    let textarea = document.getElementById('textarea-edit')
    textarea.innerText = text
    textarea.style.height =
        textarea.scrollHeight - parameter(getComputedStyle(textarea).fontSize.replace('px', ''))
        - 2 * getComputedStyle(textarea).padding.replace('px', '') + 'px'
    document.getElementsByClassName('modal-button')[0].onclick = closeModal
    document.getElementsByClassName('modal-button')[1].onclick = () => {
        edit_something(type, id, textarea.value)
        closeModal()
    }
}

function displayOptionMenu(el) {
    let data = el.target.id.split('-'); let type = data[1]; let id = data[2]
    let popover = document.getElementById(`popover-${type}-${id}`)
    if (popover) {popover.remove()}
    else {
        let any_popover = document.getElementsByClassName('popover')[0]
            if (any_popover) {any_popover.remove()}
        el.target.parentNode.parentNode.insertAdjacentHTML('beforeend', `<div id="popover-${type}-${id}" class='popover'></div>`)
        let new_popover = document.getElementById(`popover-${type}-${id}`)
        new_popover.style.setProperty('display', 'flex')
        let delete_button = `<button class="popover_button" onclick="deleteButton(this, '${type}', ${id})">delete this ${type}</button>`
        new_popover.insertAdjacentHTML("afterbegin", delete_button)
        if ((type === 'post') || (type === 'comment')) {
            let edit_button = `<button class="popover_button" onclick="editButton(this, '${type}', ${id})">edit this ${type}</button>`
            new_popover.insertAdjacentHTML("beforeend", edit_button)
        }
        window.onclick = function(event) {
            let popover = document.getElementById(`popover-${type}-${id}`)
            if ((event.target !== popover) && (event.target !== document.getElementById(`options_button-${type}-${id}`))) {
                if (popover) {popover.remove()}
            }}
        }}


function optionButtonsListeners() {
    let options_buttons = document.getElementsByClassName('options_button')
    for (let i = 0; i < options_buttons.length; i++) {
        options_buttons[i].addEventListener('click', displayOptionMenu)
    }}


$(document).ready(function() {
    optionButtonsListeners()
})
