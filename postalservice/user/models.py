from django.db import models
from django.contrib.auth.hashers import make_password

class Permission(models.Model):
    permission = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.permission

class Role(models.Model):
    role_name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.role_name

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('role', 'permission'),)  # Composite key

class User(models.Model):
    username = models.EmailField(primary_key=True, unique=True)
    password = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Hash the password
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username