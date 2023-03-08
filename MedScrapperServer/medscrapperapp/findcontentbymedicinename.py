from medscrapperapp.pharmeasy_models import MedicinePharmEasy
from medscrapperapp.netmeds_models import MedicineNetMeds
from medscrapperapp.onemg_models import Medicine1mg
from medscrapperapp.contentseparator import *
def findContentByMedicineName(medicine_name,website) :
    if website == "1mg" :
        medicine = Medicine1mg.objects.filter(name = medicine_name)
        return separatecontent1mg(medicine.content)
    elif website == "netmeds" :
        medicine = MedicineNetMeds.objects.filter(name = medicine_name)
        contents = []
        contents.append(medicine.content.replace(" ",""))
        return contents
    else :
        medicine = MedicinePharmEasy.objects.filter(name = medicine_name)
        return separatecontentPhameasy(medicine.content)