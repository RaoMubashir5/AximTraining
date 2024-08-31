from rest_framework.permissions import BasePermission

class CustomizeAPIPermissions(BasePermission):

    def has_permission(self, request, view):  #user level permissions 
               # Allow POST for authenticated users to create new records
        if request.method in ['POST','GET']:
            return request.user.is_authenticated
        
        # Allow PUT, PATCH, DELETE if user is authenticated
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user.is_authenticated


    def has_object_permission(self, request, view, obj):
           # Debugging print statements
        print(f"Request User: {request.user}")
        print(f"Object Creator: {obj.created_by}")
        
        # Allow GET, PUT, PATCH, and DELETE if user is a superuser
        # Allow PUT, PATCH, and DELETE if the user created the object
        if request.method in ['GET','PUT', 'PATCH', 'DELETE']:
            if (obj.created_by == request.user) or request.user.is_superuser:
                return True
    
        # Deny access for other methods
        return False
