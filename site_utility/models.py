from django.db import models

# Create your models here.
class Cities(models.Model):
    county = models.ForeignKey('Counties', models.DO_NOTHING)
    name = models.CharField(max_length=64)
    name_simple = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'cities'

class Counties(models.Model):
    code = models.CharField(unique=True, max_length=2)
    name = models.CharField(max_length=64)
    name_simple = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'counties'