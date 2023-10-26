from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # if request.method == 'GET':
        if request.method in permissions.SAFE_METHODS:  # it include get, head, option
            return True
        else:
            return bool(request.user and request.user.is_staff)


# class FullDjangoModelPermission(permissions.DjangoModelPermissions):
#     def __init__(self) -> None:
#         self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s'],
# # made this class for knowledge

class ViewCustomerHistoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('store.view_history')
