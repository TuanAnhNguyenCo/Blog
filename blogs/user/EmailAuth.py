from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

class SettingsBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):

        try:
            user = User.objects.get(email = email);
        except:
            return None
        if user.check_password(password):
            return user
        else:
            return None
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None