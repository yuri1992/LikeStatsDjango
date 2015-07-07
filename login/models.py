from django.db import models


class UserManager(models.Manager):

    def user_exists(self, fb_id):
        return self.filter(fb_id=fb_id).exists()


class User(models.Model):
    fb_id = models.IntegerField(primary_key=True)
    email = models.EmailField(blank=True, null=True)
    birthday = models.CharField(max_length=60, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=(
        ('m', 'Male'), ('f', 'Female')), blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    access_token = models.TextField(
        blank=True, help_text='Facebook token for offline access', null=True)
    access_token_expires = models.IntegerField()

    def get_fbid(self):
        return self.fb_id

    def get_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_access_token(self):
        return self.access_token

    objects = UserManager()
