from medscrapperapp.pharmeasy_models import MedicinePharmEasy
from medscrapperapp.netmeds_models import MedicineNetMeds
from medscrapperapp.onemg_models import Medicine1mg
from django.forms.models import model_to_dict

def get_medicine_details(content,website):
    if website == "onemg" :
        data =  Medicine1mg.objects.filter(content__icontains = content).values("id")
        return data
    elif website == "netmeds" :
        return MedicineNetMeds.objects.filter(content__icontains = content).values("id")
    return MedicinePharmEasy.objects.filter(content__icontains = content).values("id")

def get_medicine(content,website) :
    n = len(content)
    left = 0
    right = n

    while left < right :
        mid = int((left + right+1)/2)
        tempcontent = content[0:int(mid)]
       
        result = get_medicine_details(tempcontent,website)
        # print(left,right,mid,len(result))
        if mid == 1 and len(result) == 0:
            return []
        if(len(result) >= 1):
            left = mid
        else :
            right = mid-1
  
    tempcontent = content[0:int(left)]
    if website == "onemg" :
        result =  Medicine1mg.objects.filter(content__icontains = tempcontent)
    elif website == "netmeds" :
        result = MedicineNetMeds.objects.filter(content__icontains = tempcontent)
    else :
        result = MedicinePharmEasy.objects.filter(content__icontains = tempcontent)
    print(len(result))
    return result
    
def get_medicinebycontent(contents,website) :
    medicine_dict = {}
    medicine_list = {}
    
    for content in contents :
        medicines = get_medicine(content,website)
        for medicine in medicines :
            medicine_list[medicine.name] = medicine
            if medicine.name in medicine_dict :
                medicine_dict[medicine.name] = medicine_dict[medicine.name] + 1
            else :
                medicine_dict[medicine.name] = 1
    
    sorted_medicine_dict = sorted(medicine_dict.items(), key=lambda x:-x[1])[0:10]
    medicine_details = []
    for medicine in sorted_medicine_dict :
        print(medicine)
        medicine_details.append(model_to_dict(medicine_list[medicine[0]]))

    return medicine_details
