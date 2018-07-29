from ..models import UserProfile


def save_profile(backend, user, response, *args, **kwargs):

    user_details = kwargs.get('details', {})
    username = user_details.get('username')
    email = user_details.get('email')
    user_instance = UserProfile.objects.filter(username=username).exists()
    profile = None
    if not user_instance:
        profile = UserProfile(
            username=username, email=email, user_type='Customer')
        profile.save()
        return profile
    return 


# def generated_username(user, details, *args, **kwargs):
#     username = details['username']
#     user.your_field = username
#     user.save()
