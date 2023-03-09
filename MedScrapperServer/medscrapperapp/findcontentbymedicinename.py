from medscrapperapp.pharmeasy_models import MedicinePharmEasy
from medscrapperapp.netmeds_models import MedicineNetMeds
from medscrapperapp.onemg_models import Medicine1mg
from medscrapperapp.contentseparator import *
def findContentByMedicineName(medicine_name,website) :
    if website == "1mg" :
        medicine = Medicine1mg.objects.filter(name = medicine_name).values("content")
        if len(medicine) == 0 :
            return ["Not Found"]
        return separatecontent1mg(medicine[0]['content'])
    elif website == "netmeds" :
        medicine = MedicineNetMeds.objects.filter(name = medicine_name).values("content")
        contents = []
        if len(medicine) == 0 :
            return ["Not Found"]
        contents.append(medicine[0]['content'].replace(" ",""))
        return contents
    else :
        medicine = MedicinePharmEasy.objects.filter(name = medicine_name).values("content")
        if len(medicine) == 0 :
            return ["Not Found"]
        return separatecontentPhameasy(medicine[0]['content'])