from django.forms.models import model_to_dict

from medscrapperapp.subscription_models import Subscription

def giveuserbyemail(email):
    print(email['email'])
    # try:
    subscription = Subscription.objects.filter(email = email['email']).only("medicine_name")
    medicine_dict = []
    for med in subscription:
        medicine_dict.append(model_to_dict(med)) 

    return medicine_dict
    # except:
        # return "No Medicine Found"
    return "temp"