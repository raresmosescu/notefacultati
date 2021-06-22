from django.db import models
from school.models import Facultati
from user.models import AuthUser

# Create your models here.

class Profesori(models.Model):
    id_profesor = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=45)
    id_facultate = models.ForeignKey(Facultati, models.DO_NOTHING, db_column='id_facultate')
    departament = models.CharField(max_length=255, blank=True, null=True)
    disciplina = models.CharField(max_length=255, blank=True, null=True)
    numarul_notelor = models.IntegerField(blank=True, null=True)
    media_notelor = models.FloatField(blank=True, null=True)
    media_rotunjita = models.IntegerField(blank=True, null=True)
    id_creator = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='id_creator', blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profesori'


class Pareri(models.Model):
    id_parere = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='id_user')
    profesor = models.ForeignKey('Profesori', models.DO_NOTHING, db_column='profesor')
    nota_generala = models.IntegerField()
    dificultate = models.IntegerField()
    as_repeta = models.IntegerField()
    tag1 = models.IntegerField(blank=True, null=True)
    tag2 = models.IntegerField(blank=True, null=True)
    tag3 = models.IntegerField(blank=True, null=True)
    mesaj = models.CharField(max_length=254, blank=True, null=True)
    nota_primita_student = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    ip = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pareri'


class Taguri(models.Model):
    id_tag = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'taguri'


