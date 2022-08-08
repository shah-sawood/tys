from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.signals import user_logged_out
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

from tests.models import Category
from tests.models import Choice
from tests.models import Question

from users.models import Profile
from users.models import SocialLink
from users.models import Notification


# Create your signals below
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.profiles.create(user=instance)


@receiver(user_logged_in)
def make_user_online(sender, user, request, **kwargs):
    try:
        user.profile.status = True
        user.profile.save()
    except User.profile.RelatedObjectDoesNotExist:
        Profile.profiles.create(user=user, status=True)


@receiver(user_logged_out)
def make_user_offline(sender, user, request, **kwargs):
    if user is not None:
        try:
            user.profile.status = False
            user.profile.save()
        except User.profile.RelatedObjectDoesNotExist:
            Profile.profiles.create(user=user)
