from django.db import models


class Golfer(models.Model):
    golfer_id = models.AutoField(primary_key=True)
    golfer_fname = models.CharField(max_length=50)
    golfer_lname = models.CharField(max_length=50)
    golfer_mi = models.CharField(max_length=10, blank=True, null=True)
    default_salary = models.IntegerField()
    original_salary = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'golfer_t'

    def __unicode__(self):
        return unicode(self.golfer_lname + ', ' + self.golfer_fname)