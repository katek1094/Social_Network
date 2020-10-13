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
        //    TODO: delete from the page
        }
    });
}


function openModal(type, where) {
    let modal = `<div id="modal">
                        <div class="modal-box">
                            <div class="modal-header">
                                <p class="modal-title">Delete ${type}</p>
                                <span id="modal-close">&times;</span>
                            </div>
                            <div class="modal-content">
                                <p>are you sure you want to delete this ${type}?</p>
                                <div class="modal-buttons">
                                    <button class="modal-button cancel">cancel</button>
                                    <button class="modal-button delete">delete</button>
                                </div></div></div></div>`
    where.insertAdjacentHTML('afterend', modal)
    modal = document.getElementById('modal')
    modal.style.setProperty('display', 'flex')
    document.body.style.overflow = 'hidden'
}


function closeModal () {
    document.getElementById('modal').remove()
    document.body.style.overflow = 'initial'
}


function deleteButton(el, type, id) {
    openModal(type, el.parentNode)
    document.getElementById('modal-close').onclick = closeModal
    window.onclick = function(event) {
        if (event.target === document.getElementById('modal')) {
            closeModal()
        }}
    document.getElementsByClassName('modal-button')[0].onclick = closeModal
    document.getElementsByClassName('modal-button')[1].onclick = () => {delete_something(type, id)}
}


function displayOptionMenu(el) {
    let data = el.target.id.split('-'); let type = data[1]; let id = data[2]
    let popover = document.getElementById(`popover-${type}-${id}`)
    if (popover) {popover.remove()}
    else {
        el.target.parentNode.parentNode.insertAdjacentHTML('beforeend', `<div class="popover" id='popover-${type}-${id}'></div>`)
        let new_popover = document.getElementById(`popover-${type}-${id}`)
        new_popover.style.setProperty('display', 'flex')
        let delete_button = `<button class="delete_button" onclick="deleteButton(this, '${type}', ${id})">delete this ${type}</button>`
        new_popover.insertAdjacentHTML("afterbegin", delete_button)
    }}


function optionButtonsListeners() {
    let options_buttons = document.getElementsByClassName('options_button')
    for (let i = 0; i < options_buttons.length; i++) {
        options_buttons[i].addEventListener('click', displayOptionMenu)
    }}


$(document).ready(function() {
    optionButtonsListeners()
})
