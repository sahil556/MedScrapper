from medscrapperapp.pharmeasy_models import MedicinePharmEasy
from medscrapperapp.netmeds_models import MedicineNetMeds
from medscrapperapp.onemg_models import Medicine1mg
from django.forms.models import model_to_dict


def get_medicine_details(name1,website):
    if website == "onemg" :
        data =  Medicine1mg.objects.filter(name__icontains = name1).values("id")
        return data
    elif website == "netmeds" :
        return MedicineNetMeds.objects.filter(name__icontains = name1).values("id")
    return MedicinePharmEasy.objects.filter(name__icontains = name1).values("id")

def get_medicine(name,website) :
    n = len(name)
    left = 0
    right = n

    while left < right :
        mid = int((left + right+1)/2)
        tempname = name[0:int(mid)]
        result = get_medicine_details(tempname,website)
        print(left,right,mid,len(result))
        if(len(result) >= 1):
            left = mid
        else :
            right = mid-1
  
    tempname = name[0:int(left)]
    if website == "onemg" :
        result =  Medicine1mg.objects.filter(name__icontains = tempname)
    elif website == "netmeds" :
        result = MedicineNetMeds.objects.filter(name__icontains = tempname)
    else :
        result = MedicinePharmEasy.objects.filter(name__icontains = tempname)
    print("From Pharmeasy", len(result),result)
    medicine_details = []
    for res in result :
        medicine_details.append(model_to_dict(res))

    return medicine_details
    
