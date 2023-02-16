from django.db import models

# Create your models here.
class Subscription(models.Model):
    email = models.CharField(blank = True, null =True, max_length = 50)
    medicine_name = models.CharField(blank = True, null =True, max_length = 50)
    website_name = models.CharField(blank = True, null =True, max_length = 50)
    