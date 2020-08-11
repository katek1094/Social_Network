
function friendshipButton(auth_profile_user_id, visited_profile_user_id) {
    let button = document.getElementById('friendship-button')
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
    });
}