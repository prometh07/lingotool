from django.contrib.auth.models import Group, User
from django.dispatch import receiver

from registration.signals import user_registered

@receiver(user_registered)
def user_registered_callback(sender, user, request, **kwargs):
    #default_user = Group.objects.get(name='default_user')
    #user.groups.add(default_user)
    #user.save()
    # standard django groups don't work with django-nonrel and gae
    pass
