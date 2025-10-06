from rest_framework.viewsets import ModelViewSet

class ActionSerializerPermissionMixin:
    """
    Support action-specific serializer and permission mapping.
    - action_serializer_classes: dict[action_name] = SerializerClass
    - action_permission_classes: dict[action_name] = [PermissionClasses...]
    If action not present -> fallback to serializer_class and permission_classes.
    """
    action_serializer_classes = {}
    action_permission_classes = {}

    def get_serializer_class(self):
        return self.action_serializer_classes.get(self.action, self.serializer_class)

    def get_permissions(self):
        perms = self.action_permission_classes.get(self.action, self.permission_classes)
        return [p() for p in perms]