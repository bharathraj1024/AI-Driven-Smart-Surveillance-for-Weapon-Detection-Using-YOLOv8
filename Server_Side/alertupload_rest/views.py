from alertupload_rest.serializers import UploadAlertSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from threading import Thread
from django.core.mail import send_mail
import re
import os
import datetime
from twilio.rest import Client
from django.conf import settings

def start_new_thread(function):
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator

@api_view(['POST'])
def post_alert(request):
    serializer = UploadAlertSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        print("🔗 Image URL:", serializer.data['image'])  # 👈 Add this line
        identify_email_sms(serializer)
    else:
        return JsonResponse({'error': 'Unable to process data!'}, status=400)

    return Response(request.META.get('HTTP_AUTHORIZATION'))


def identify_email_sms(serializer):
    if re.search(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', serializer.data['alert_receiver']):
        print("Valid Email")
        send_email(serializer)

    elif re.match(r'^\+91[6789]\d{9}$', serializer.data['alert_receiver']):  
        # Matches +91 followed by a 10-digit number starting with 6, 7, 8, or 9
        print("Valid Indian Mobile Number")
        send_sms(serializer)

    else:
        print("Invalid Email or Mobile Number")

@start_new_thread
def send_email(serializer):
    send_mail(
        'Weapon Detected!', 
        prepare_alert_message(serializer), 
        'weapondetectionsystem25@gmail.com',
        [serializer.data['alert_receiver']],
        fail_silently=False,)
    
@start_new_thread
def send_sms(serializer):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(body=prepare_alert_message(serializer),
                                    from_=settings.TWILIO_NUMBER,
                                    to=serializer.data['alert_receiver'])

def prepare_alert_message(serializer):
    """ Generates an alert message with the correct URL. """
    image_path = serializer.data.get('image', '').strip()  # Get image filename safely

    if not image_path:
        return 'Error: No image provided'

    # Extract UUID (Remove directories & extension)
    uuid = os.path.splitext(os.path.basename(image_path))[0].strip()

    if not uuid:
        return 'Error: Invalid image filename'

    url = f'http://127.0.0.1:8000/alert/{uuid}'  # ✅ Correct URL format
    #return f'Weapon Detected! View alert at {url}'
    return f'Weapon Detected! Be Cautious'



