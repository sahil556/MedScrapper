
class MedicineDetails:
    def __init__(self, name, price, imglink, content, sideeffect, manufacturer, howtouse, description, medlink):
        self.name = name
        self.price = price
        self.imglink = imglink
        self.content = content
        self.sideeffect = sideeffect
        self.manufacturer = manufacturer
        self.howtouse = howtouse
        self.description = description
        self.medlink = medlink
   
    def printdetails(self):
        print(f'Name: {self.name} \nPrice: {self.price} \nImage Link: {self.imglink} \nContent: {self.content} \nSide Effect: {self.sideeffect} \nManufacturer: {self.manufacturer} \nHow to use: {self.howtouse} \nDescription: {self.description} \nMedicine Link: {self.medlink}')
