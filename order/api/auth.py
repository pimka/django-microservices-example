from rest_framework.authentication import TokenAuthentication
from api.models import CustomToken
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from django.utils import timezone
from datetime import timedelta

class TokenAuth(TokenAuthentication):
    model = CustomToken
    keyword = 'Bearer'

    def authenticate_credentials(self, token):
        try:
            model_token = self.model.objects.get(token=token)
        except self.model.DoesNotExist:
            raise AuthenticationFailed('Invalid token')
        
        time_elapsed = timezone.now() - model_token.created_time
        time_left = timedelta(seconds=3600) - time_elapsed

        if time_left < timedelta(seconds=0):
            model_token.delete()
            raise NotAuthenticated('Token has expired')

        return (None, model_token)