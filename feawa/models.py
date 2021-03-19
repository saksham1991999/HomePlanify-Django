from django.db import models


class Zone(models.Model):
    name = models.CharField(max_length=256)
    areas = models.TextField()


bloodgroup_choices = (
    ("A-", "A-"),
    ("A+", "A+"),
    ("B-", "B-"),
    ("B+", "B+"),
    ("O+", "O+"),
    ("O-", "O-"),
    ("AB-", "AB-"),
    ("AB+", "AB+"),
)


class Firm(models.Model):
    user = models.OneToOneField("core.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    email = models.EmailField()
    firm_name = models.CharField(max_length=256)
    zone = models.ForeignKey("feawa.Firm", on_delete=models.CASCADE)
    deals = models.TextField()
    office_address = models.TextField()
    home_address = models.TextField()
    phone = models.CharField(max_length=15)
    bloodgroup = models.CharField(max_length=3, choices=bloodgroup_choices)