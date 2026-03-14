from rest_framework.permissions import BasePermission
from diet_app.models import User
class IsOwner(BasePermission):
    message = "user should be owner"
    def has_object_permission(self, request, view, obj):

        if isinstance(obj,User):

            return request.user == obj

        return obj.owner ==  request.user
    

class HasUserProfile(BasePermission):

    message = "User has no profile"
    def has_permission(self, request, view):
        
        try:

            profile = request.user.profile

            return True

        except:

            return False