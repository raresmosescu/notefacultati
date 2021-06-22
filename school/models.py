from django.db import models

# Create your models here.
class Facultati(models.Model):
    id_facultate = models.AutoField(primary_key=True)
    facultate = models.CharField(max_length=255)
    universitate = models.CharField(max_length=255)
    localitate = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'facultati'


class Specializari(models.Model):
    id_specializare = models.AutoField(primary_key=True)
    id_facultate = models.ForeignKey(Facultati, models.DO_NOTHING, db_column='id_facultate')
    specializare = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'specializari'