from rest_framework import permissions 

# BasePermission includes functions about the permissions in the database 
class Is_owner(permissions.BasePermission):
    # to return True or False if the user of object in the base view is same with the requested user
    def object_permission(self, request, view, obj):
        return obj.user==request.user
    
