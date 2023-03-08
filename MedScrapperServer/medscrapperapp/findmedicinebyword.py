from medscrapperapp.pharmeasy_models import MedicinePharmEasy
from medscrapperapp.netmeds_models import MedicineNetMeds
from medscrapperapp.onemg_models import Medicine1mg

def get_medicine_details(name1,website):
    if website == "onemg" :
        return Medicine1mg.objects.filter(name__icontains = name1) 
    elif website == "netmeds" :
        return MedicineNetMeds.objects.filter(name__icontains = name1)
    return MedicinePharmEasy.objects.filter(name__icontains = name1)

def get_medicine(name,website) :
    n = len(name)
    left = 0
    right = n

    while left < right :
        mid = int((left + right)/2)
        tempname = name[0:int(mid)]
        result = get_medicine_details(tempname,website)
        # print(left,right,mid,len(result))
        if(len(result) >= 1):
            left = mid+1
        else :
            right = mid-1
    print(left,right)
  
    tempname = name[0:int(left)]
    result = get_medicine_details(tempname,website)
    print("From Pharmeasy", len(result),result)
    for res in result :
        print(res.name)
    return result
    
