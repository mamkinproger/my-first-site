from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=254, blank=True, verbose_name='Email', unique=True)

    def __str__(self):
        return self.user


class DeviceStandart(models.Model):
    type = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'device_standart'

    def __str__(self):
        return self.type


class Device(models.Model):
    name = models.TextField(blank=True, null=True)
    standarts = models.ManyToManyField(DeviceStandart, through='DeviceStandartToDevice')
    state = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'device'

    def __str__(self):
        return self.name


class DeviceStandartToDevice(models.Model):
    deviceid = models.ForeignKey(Device, models.CASCADE,
                                    db_column='deviceid', blank=True, null=True)
    devicestandartid = models.ForeignKey(DeviceStandart, models.CASCADE,
                                            db_column='devicestandartid', blank=True, null=True, )

    class Meta:
        managed = True
        db_table = 'device_standart_to_device'


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
