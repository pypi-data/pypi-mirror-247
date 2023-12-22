This app includes DjangoEnum class which compatible with Django choice fields.

Usage example::


    from django.db import models
    from django_enum import DjangoEnum


    class StatusTypes(DjangoEnum):
        ACTIVE = 0
        STOPPING = 1
        STOPPED = 2


    class MyModel(models.Model):
        status = models.IntegerField(choices=StatusTypes.choices())

