from django.db import models
from lib.national_id import NationalID
# Create your models here.
class User(models.Model):
    email = models.EmailField(max_length=254)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    national_id = models.CharField(unique=True, primary_key=True , max_length=20)
    password = models.CharField(max_length=50)
    balance = models.FloatField()
    date_of_creation = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to="usersImage/")
    governorate = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Transfers(models.Model):
    from_user = models.ForeignKey(User, related_name='transfers_from', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='transfers_to', on_delete=models.CASCADE)
    balance = models.FloatField()
    date_of_process = models.DateField(auto_now_add=True)