from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Permission
@receiver(post_migrate)
def create_default_permissions(sender, **kwargs):
    if sender.name == 'user':  # Replace with your actual app name
        permissions = ['can_view', 'can_edit', 'can_delete']
        for perm_name in permissions:
            Permission.objects.get_or_create(permission=perm_name)