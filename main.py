import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from bs4 import BeautifulSoup
import time
import logging

port = 465  # for SSL
smtp_server = "smtp.gmail.com"
sender_email = "bpgappdev@gmail.com"
sender_password = "EnterYourOwn"
lacey_email = "EnterYourOwn"
test_email = "EnterYourOwn"
receiver_email = lacey_email

message = MIMEMultipart("alternative")
message["Subject"] = "HURRY, A PLANT IS IN STOCK!"
message["From"] = sender_email
message["To"] = receiver_email
message["X-Priority"] = "2"


threeIncherInStock = """\
Hi,
View the 3" Philodendron Rio here: 
https://www.gabriellaplants.com/collections/philodendron/products/3-philodendron-rio?_pos=1&_sid=5f26d33de&_ss=r 
Better hurry, these suckers are flying off the shelf!
"""
threeIncherInStockHtml = """\
<html>
  <body>
    <p>Hi,<br>
       View the 3" Philodendron Rio <a href="https://www.gabriellaplants.com/collections/philodendron/products/3-philodendron-rio?_pos=1&_sid=5f26d33de&_ss=r">Here</a> <br>
       Better hurry, these suckers are flying off the shelf!
    </p>
  </body>
</html>
"""
fourIncherInStock = """\
Hi,
View the 4" Philodendron Rio here: 
https://www.gabriellaplants.com/collections/philodendron/products/rio-philodendron-4-original-consistent-collectors-version-of-brasil-philodendron-silver-variegation?_pos=2&_sid=5f26d33de&_ss=r 
Better hurry, these suckers are flying off the shelf!
"""
fourIncherInStockHtml = """\
<html>
  <body>
    <p>Hi,<br>
       View the 4" Philodendron Rio <a href="https://www.gabriellaplants.com/collections/philodendron/products/rio-philodendron-4-original-consistent-collectors-version-of-brasil-philodendron-silver-variegation?_pos=2&_sid=5f26d33de&_ss=r">Here</a> <br>
       Better hurry, these suckers are flying off the shelf!
    </p>
  </body>
</html>
"""

part1 = MIMEText(threeIncherInStock, "plain")
part2 = MIMEText(threeIncherInStockHtml, "html")
part3 = MIMEText(fourIncherInStock, "plain")
part4 = MIMEText(fourIncherInStockHtml, "html")


def threeinchstockcheck():
    data = requests.get('https://www.gabriellaplants.com/collections/philodendron/products/3-philodendron-rio?_pos=1&_sid=2efee07e7&_ss=r')
    soup = BeautifulSoup(data.text, 'html.parser')
    for script in soup.find_all('script', {'id': 'stockify-json-data'}):
        strippedstring = repr(script.string)
        indexof = strippedstring.find('"available":')
        print("The availability of the 3 incher has status: " + strippedstring[indexof+12:indexof+17])
        if strippedstring[indexof + 12:indexof + 17] != "false":
            message.attach(part1)
            message.attach(part2)
            return 1


def fourinchstockcheck():
    data2 = requests.get('https://www.gabriellaplants.com/collections/philodendron/products/rio-philodendron-4-original-consistent-collectors-version-of-brasil-philodendron-silver-variegation?_pos=2&_sid=5f26d33de&_ss=r')
    soup2 = BeautifulSoup(data2.text, 'html.parser')
    script = soup2.find('span', {'class': 'available value'})
    scriptiwant = script.find_next('span', {'class': 'js_in_stock'})
    print(scriptiwant.string)
    # scriptiwant2 = scriptiwant.find_next('script', {'type': 'application/ld+json'})
    if scriptiwant.string == 'none':
        print('test')
    # strippedstring2 = repr(scriptiwant.string)
    # indexof2 = strippedstring2.find('"availability" :')
    # print("The availability of the 4 incher has status: " + strippedstring2[indexof2+36:indexof2+46])
    # if strippedstring2[indexof2 + 18:indexof2+46] != "http://schema.org/OutOfStock":
    #     message.attach(part3)
    #     message.attach(part4)
    #     return 1


def main():
    sentfirst = False
    sentsecond = False
    while True:
        if threeinchstockcheck() == 1:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, message.as_string())
                sentfirst = True
                if sentsecond:
                    break
            if fourinchstockcheck() == 1:
                server.sendmail(sender_email, receiver_email, message.as_string())
                break
        if fourinchstockcheck() == 1:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, message.as_string())
                sentsecond = True
                if sentfirst:
                    break
            if threeinchstockcheck() == 1:
                server.sendmail(sender_email, receiver_email, message.as_string())
                break
        time.sleep(60)


main()
