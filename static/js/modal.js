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




function deleteButton(el, type, id) {
  let new_modal = `<div id="modal-${type}-${id}" class="modal">
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
                                </div>
                            </div>
                        </div>
                    </div>`
  el.parentNode.insertAdjacentHTML('afterend', new_modal)
  new_modal = document.getElementById(`modal-${type}-${id}`)
  new_modal.style.setProperty('display', 'flex')
  document.body.style.overflow = 'hidden'
  function close_modal () {
    new_modal.remove()
    document.body.style.overflow = 'initial'
  }
  document.getElementById('modal-close').onclick = close_modal
  window.onclick = function(event) {
    if (event.target === new_modal) {
      close_modal()
    }}
  document.getElementsByClassName('modal-button')[0].onclick = close_modal
  document.getElementsByClassName('modal-button')[1].onclick = function () {
    $.ajax({
        url: delete_url.replace('type', type).replace('2137', id),
        type: 'DELETE',
        data: {
          type: type,
          id: id,
        },
        dataType: 'json',
        beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                },
        success: function (response) {
        //    TODO: delete from the page
          console.log('success xd')
        }
    });
  }


}


function displayOptionMenu(el) {
  let data = el.target.id.split('-')
  let type = data[1]
  let id = data[2]
  let popover = document.getElementById(`popover-${type}-${id}`)
  if (popover) {
    popover.remove()
  }
  else {
    el.target.parentNode.parentNode.insertAdjacentHTML('beforeend', `<div class="popover" id='popover-${type}-${id}'></div>`)
    let new_popover = document.getElementById(`popover-${type}-${id}`)
    new_popover.style.setProperty('display', 'flex')
    let delete_button = `<button class="delete_button" onclick="deleteButton(this, '${type}', ${id})">delete this ${type}</button>`
    new_popover.insertAdjacentHTML("afterbegin", delete_button)
  }
}

$(document).ready(function() {
  let options_buttons = document.getElementsByClassName('options_button')
  for (let i = 0; i < options_buttons.length; i++) {
    options_buttons[i].addEventListener('click', displayOptionMenu)
  }
})
