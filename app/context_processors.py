from .models import UserProfile, FriendRequest


def auth_profile_user(request):
    if request.user.is_authenticated:
        auth_profile_user = UserProfile.objects.get(user=request.user)
        friend_requests = FriendRequest.objects.filter(receiver=auth_profile_user)
        friend_requests_number = len(friend_requests)

        return {'auth_profile_user': auth_profile_user, "friend_requests_number": friend_requests_number}
    return {"auth_profile_user": 0}



