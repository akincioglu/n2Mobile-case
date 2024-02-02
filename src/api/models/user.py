from django.db import models

class Geo(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()

class Address(models.Model):
    street = models.CharField(max_length=255)
    suite = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=20)
    geo = models.OneToOneField(Geo, on_delete=models.CASCADE)

class Company(models.Model):
    name = models.CharField(max_length=255)

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    website = models.URLField()
    company = models.OneToOneField(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.username