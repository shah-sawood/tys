from django.contrib.auth.models import User
from django.db import models


from tests.models import Category
from tests.models import Question

# Create your models here.
class Profile(models.Model):
    """docstring for profile"""

    statuses = ((True, "Online"), (False, "Offline"))

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to="static/users/images/", default="static/images/default.jpg"
    )
    status = models.BooleanField(default=False, choices=statuses)
    bio = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def get_user(self):
        return self.user

    def get_profile_pic(self):
        return self.profile_pic

    def get_profile_pic_url(self):
        return self.profile_pic().url

    def get_social_links(self):
        return self.social_links.all()

    def get_status(self):
        return self.status

    def get_bio(self):
        """returns bio of this profile"""
        return self.bio

    def get_date_created(self):
        """returns the creation date of this profile"""
        return self.date_created

    def get_date_updated(self):
        return self.date_updated

    def __str__(self):
        return "{}".format(self.get_user().get_username())

    profiles = models.Manager()


class SocialLink(models.Model):
    """docstring for profile"""

    profile = models.ForeignKey(
        Profile, related_name="social_links", on_delete=models.CASCADE
    )
    link = models.URLField()
    date_created = models.DateTimeField(auto_now_add=True)

    sociallinks = models.Manager()

    def get_profile(self):
        return self.profile

    def get_link(self):
        return self.link

    def get_date_created(self):
        return self.date_created


class Notification(models.Model):
    """docstring for profile"""

    notifier = models.ForeignKey(
        User, related_name="notifications", on_delete=models.CASCADE
    )
    message = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    notifications = models.Manager()

    def get_notifier(self):
        return self.notifier

    def get_message(self):
        return self.message

    def get_question(self):
        return self.question

    def get_category(self):
        return self.category

    def get_is_read(self):
        return self.is_read

    def get_date_created(self):
        return self.date_created
