import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS="harshadjaviya0@gmail.com"
EMAIL_PASSWORD="duebtxtdklakzbum"

def send_mail(email, old_details, new_price) :
    msg = EmailMessage()
    msg['Subject'] = 'Medicine Price Alert ! '
    msg['From'] = 'harshadjaviya0@gmail.com'
    msg['To'] = email
    if old_details.imglink is list :
        old_details.imglink = old_details.imglink[0]
    print(type(old_details.imglink))
    msg.set_content('''
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <style></style>
    </head>
    <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif">
        <center>
        <div
            class="card"
            style="
            background-color: rgb(255, 255, 255);
            border: 1px solid #ccc;
            max-width: 400px;
            "
        >
            <p
            style="
                margin-top: 0px;
                font-size: 20px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                letter-spacing: 0.5px;
                padding: 10px;
                background-color: whitesmoke;
            "
            >
            '''+ old_details.name+'''
            </p>
            <img
            src="'''+ old_details.imglink +'''"
            style="border-radius: 5px"
            class="card-img-top"
            alt="..."
            />
            <div class="card-body">
            <!-- <hr/ -->
            <p
                style="
                text-align: justify;
                letter-spacing: 0.7px;
                padding: 0px 20px;
                "
            >
                Old Price :- '''+ str(old_details.price) +''' <br /><small style="font-size: 17px; font-weight: 500"
                >New Price :- ''' + str(new_price)+ ''' 
                </small>
            </p>

            <p
                style="
                text-indent: 1px;
                text-align: justify;
                padding: 0px 20px;
                letter-spacing: 0.7px;
                "
            >
                Description :-
            </p>
            <p
                style="
                text-indent: 10px;
                text-align: justify;
                letter-spacing: 0.7px;
                padding: 10px 20px;
                "
            >''' + old_details.description+'''
            </p>

            <a href="'''+ old_details.medlink +'''" class="btn btn-primary" style="padding-bottom: 10px"
                >Go to Full Details.</a
            >
            <br />
            <br />
            </div>
        </div>
        </center>
    </body>
    </html>

    ''', subtype='html')




    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('harshadjaviya0@gmail.com', "duebtxtdklakzbum") 
        smtp.send_message(msg)