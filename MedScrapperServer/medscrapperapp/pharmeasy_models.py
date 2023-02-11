from django.db import models

# Create your models here.
class MedicinePharmEasy(models.Model):
    name = models.CharField(blank = True, null =True, max_length = 100)
    price = models.CharField(blank = True, null =True, max_length = 30)
    imglink = models.CharField(blank = True, null =True, max_length = 1000)
    content = models.CharField(blank = True, null =True, max_length = 500)
    sideeffect = models.CharField(blank = True, null =True, max_length = 2000)
    manufacturer = models.CharField(blank = True, null =True, max_length = 50)
    howtouse = models.CharField(blank = True, null =True, max_length = 2000)
    description = models.CharField(blank = True, null =True, max_length = 3000)
    medlink = models.CharField(blank = True, null =True, max_length = 1000)