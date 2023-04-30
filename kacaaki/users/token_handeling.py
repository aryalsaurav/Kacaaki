from .models import Token
from django.utils import timezone

def update_token():
    try:
        token = Token.objects.filter(expiration_date__lte=timezone.now())
        if token.exists():
            token.delete()
    except:
        print("Error in deleting token")
        
