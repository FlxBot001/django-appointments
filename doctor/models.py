from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.http import request
from django.contrib.auth.models import User


class Profile(models.Model):
    COUNTRY_CHOICES = [
        ("KE", "Kenya"),
        ("UG", "Uganda"),
        ("US", "United States"),
        ("UK", "United Kingdom"),
        ("DE", "Germany"),
        ("HR", "Croatia"),
        ("SG", "Singapore"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    
    def __str__(self):
        return self.user.username

class Appointment(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    request = models.TextField(blank=True)
    sent_date = models.DateField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    accepted_date = models.DateField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.first_name
    
    class Meta:
        ordering = ["-sent_date"]

class Doctor(models.Model):
    medical_id = models.CharField(max_length=20, unique=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=15)
    specialization = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    attachments = models.FileField(upload_to='attachments/', blank=True, null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"