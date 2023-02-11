from django.db import models


class MedicineDetails(models.Model):
    def __init__(self, name, price, imglink, content, sideeffect, manufacturer, howtouse, description, medlink):
        # self.name = name
        # self.price = price
        # self.imglink = imglink
        # self.content = content
        # self.sideeffect = sideeffect
        # self.manufacturer = manufacturer
        # self.howtouse = howtouse
        # self.description = description
        # self.medlink = medlink
        self.name = models.CharField(blank = True, null =True, max_length = 100)
        self.price = models.CharField(blank = True, null =True, max_length = 30)
        self.imglink = models.CharField(blank = True, null =True, max_length = 1000)
        self.content = models.CharField(blank = True, null =True, max_length = 300)
        self.sideeffect = models.CharField(blank = True, null =True, max_length = 500)
        self.manufacturer = models.CharField(blank = True, null =True, max_length = 50)
        self.howtouse = models.CharField(blank = True, null =True, max_length = 2000)
        self.description = models.CharField(blank = True, null =True, max_length = 3000)
        self.medlink = models.CharField(blank = True, null =True, max_length = 500)
   
    def printdetails(self):
        print(f'Name: {self.name} \nPrice: {self.price} \nImage Link: {self.imglink} \nContent: {self.content} \nSide Effect: {self.sideeffect} \nManufacturer: {self.manufacturer} \nHow to use: {self.howtouse} \nDescription: {self.description} \nMedicine Link: {self.medlink}')
