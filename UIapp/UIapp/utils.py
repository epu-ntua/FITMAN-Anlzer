from django.contrib.auth.models import User, Group, Permission


def user_is_allowed_to_change_the_project(username, group_name):

    if group_name and username:
        user = User.objects.get(username=username)

        if user.groups.filter(name=group_name).exists() and user.is_staff:
            return True
    else:
        return False