from django.conf import settings
from ippanel import Client, Error, HTTPError, ResponseCode

def send_otp(phone_number, otp):
    
    client = Client("8en9TUYaGHPVU-gCdUSCCe4XxHuZhZUp62SQTIkY7ho=")
    ptrn = {
        'code': otp
        }

    client.send_pattern('zz9qp2vzfbtairt', "+983000505", str(phone_number), ptrn)
        
    return True

def send_sms(phone_number, ptrn):
    client = Client("8en9TUYaGHPVU-gCdUSCCe4XxHuZhZUp62SQTIkY7ho=")
    for num in phone_number:
        client.send_pattern('bxzxz3df41xdvfm', "+983000505", str(num), ptrn)