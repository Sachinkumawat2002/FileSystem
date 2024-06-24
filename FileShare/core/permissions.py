from .authentications import *
from rest_framework.permissions import BasePermission
from Customer.models import *
from Customer.serializers import *
class UserAuth(BasePermission):
    def has_permission(self, request, view):
        respond = Auth(User , request ,SignupSerializer )
        if respond.status_code == status.HTTP_200_OK:
            request.user  = respond.data
            # print(request.user)
            return True
        else:
            return False

