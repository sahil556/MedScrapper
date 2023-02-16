import smtplib
import os
import imghdr
from email.message import EmailMessage

EMAIL_ADDRESS="harshadjaviya0@gmail.com"
EMAIL_PASSWORD="duebtxtdklakzbum"

def send_mail(email, old_details, new_price) :
    print("mail done , ", email,old_details,new_price)
    contacts=[email]
    msg=EmailMessage()
    msg['subject']="Price Alert ! in" + old_details.name
    msg['From']=EMAIL_ADDRESS
    msg['To']=','.join(contacts)
    msg.set_content('old price = ' + str(old_details.price) + "new price = " + str(new_price) + "\n"+old_details.medlink)
    files=['image1.jpg','image2.jpg','image3.jpg']
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        smtp.send_message(msg)
        print("sent...")
# for file in files:
#     with open('D:/javiya/bg.jpg','rb') as f:
#         file_data=f.read()
#         file_type=imghdr.what(f.name)
#         file_name=f.name
#     #for pdf change maintype='application' subtype='octet-stream and remove file_type
#     msg.add_attachment(file_data,maintype='image',subtype=file_type,filename=file_name)



