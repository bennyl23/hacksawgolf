from django.db import models
from tinymce.models import HTMLField
import datetime


class Blog(models.Model):
    entry_id = models.AutoField(primary_key=True)
    entry_date = models.DateTimeField()
    entry_subject = models.CharField(max_length=255)
    entry_body = HTMLField()

    class Meta:
        db_table = 'blog_t'

    def __unicode__(self):
        return unicode(self.entry_subject)

    def save(self, *args, **kwargs):
        self.entry_date = datetime.datetime.now()

        super(Blog, self).save(*args, **kwargs)


