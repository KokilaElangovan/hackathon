from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


def dict_to_choice(input_dict):
    return input_dict.items()

CHECKUP_STATUS = {
    1: 'Requested',
    2: 'Accepted',
    3: 'Checked-up'
}

class Specialities(models.Model):
    speciality = models.CharField(max_length=200, default='')


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=(
        ('m', 'Male'), ('f', 'Female')))
    age = models.IntegerField(null=True, blank=True)
    blood_group =  models.CharField(max_length=5, default='')
    mobile_number = models.CharField(max_length=10, default='')
    location = models.CharField(max_length=100, default='')
    height = models.CharField(max_length=20, default='')
    hospital_name = models.CharField(max_length=20, default='')
    public_key = models.CharField(max_length=200, default='')
    address = models.TextField(default='')
    experiance = models.IntegerField(null=True, blank=True)
    speciality_id = models.OneToOneField(Specialities, unique=True, null=True, blank=True)


class DoctorPatientMapping(models.Model):
    doctor = models.ForeignKey(User, related_name='doctor_mapping_id')
    patient = models.ForeignKey(User, related_name='patient_mapping_id')
    status = models.PositiveIntegerField(choices=dict_to_choice(CHECKUP_STATUS), default=1)
    check_up_time = models.DateTimeField(null=True, blank=True)
    hospital_location = models.CharField(max_length=100, default='')
