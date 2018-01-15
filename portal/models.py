from __future__ import unicode_literals
from django.db import models


class Cost(models.Model):
    institute_id = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    room_number = models.CharField(max_length=20)
    bhavan = models.CharField(max_length=20)
    cost_list_looters = models.CharField(max_length=1000)
    cost_list_mess = models.CharField(max_length=1000)
    cost_list_fk = models.CharField(max_length=1000)
    cost_list_anc = models.CharField(max_length=1000)
    cost_list_others = models.CharField(max_length=1000)
    email = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s" % self.name


class Bus(models.Model):
    institute_id = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    seat_number = models.CharField(max_length=10)
    has_cancelled = models.BooleanField()
    bus_time = models.CharField(max_length=1)
    destination = models.CharField(max_length=1)
    date_of_bus = models.CharField(max_length=20)

    def __unicode__(self):
        return "%s --- %s" % (self.seat_number, self.date_of_bus)
