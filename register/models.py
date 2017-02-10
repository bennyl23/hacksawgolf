from django.db import models
from django.contrib.auth.hashers import make_password


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_email = models.CharField(max_length=50)
    user_password = models.CharField(max_length=128, editable=False)
    user_referring_email = models.CharField(max_length=50)
    user_team_name = models.CharField(max_length=20)
    user_af1 = models.CharField(max_length=30, blank=True)
    user_af2 = models.CharField(max_length=30, blank=True)
    user_real_name = models.CharField(max_length=50, blank=True)
    user_paid = models.BooleanField(default=False)
    message_from_commish = models.TextField(blank=True)
    user_reset_password = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'user_t'

    def __unicode__(self):
        return unicode(self.user_team_name + ', ' + self.user_email)

    def hash_password(self):
        return make_password(self.user_password)
