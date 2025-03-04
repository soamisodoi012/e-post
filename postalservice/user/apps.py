from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
#from .models import Permission can not import directely in apps

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
    def ready(self):
        import user.permissionConf