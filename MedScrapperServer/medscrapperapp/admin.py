from django.contrib import admin
from medscrapperapp.netmeds_models import MedicineNetMeds
from medscrapperapp.pharmeasy_models import MedicinePharmEasy
from medscrapperapp.onemg_models import Medicine1mg
from medscrapperapp.subscription_models import Subscription

# Register your models here.
admin.site.register(Medicine1mg)
admin.site.register(MedicineNetMeds)
admin.site.register(MedicinePharmEasy)
admin.site.register(Subscription) 