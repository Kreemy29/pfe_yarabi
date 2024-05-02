from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import JSONField


class CustomUser(AbstractUser):
    # Add common fields to all users here if needed
    # For example, you might want to add phone number or address fields to all user types
    pass


class AdminUser(CustomUser):
    # Admin specific fields
    can_create_accounts = models.BooleanField(default=True)
    can_assign_roles = models.BooleanField(default=True)
    can_edit_files = models.BooleanField(default=True)
    can_view_dashboard = models.BooleanField(default=True)
    can_import_files = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Admin User'
        verbose_name_plural = 'Admin Users'
        permissions = [
            ("can_manage_all", "Can manage everything"),
        ]

class GestionnaireUser(CustomUser):
    # Gestionnaire specific fields
    can_edit_files = models.BooleanField(default=True)
    can_view_dashboard = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Gestionnaire User'
        verbose_name_plural = 'Gestionnaire Users'
        permissions = [
            ("can_edit_files", "Can edit files"),
            ("can_view_dashboard", "Can view dashboard"),
        ]

class ConsultantUser(CustomUser):
    # Consultant specific fields
    can_view_dashboard = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Consultant User'
        verbose_name_plural = 'Consultant Users'
        permissions = [
            ("can_view_dashboard", "Can view dashboard"),
        ]


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'categories'  # Name of your table in MySQL

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'subcategories'  # Name of your table in MySQL

    def __str__(self):
        return self.name
