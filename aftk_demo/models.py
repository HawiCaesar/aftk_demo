from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Dispense_Drug_List(models.Model):

	patient_first_name = models.CharField(max_length=70)
	patient_last_name = models.CharField(max_length=70)
	date_picked = models.DateField()
	weeks_reminder = models.IntegerField(default=0)
	two_day_reminder = models.IntegerField(default=0)
	one_day_later_reminder = models.IntegerField(default=0)

