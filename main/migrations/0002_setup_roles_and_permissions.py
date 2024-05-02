from django.db import migrations
from django.contrib.auth.models import Group, Permission

def create_user_groups_and_permissions(apps, schema_editor):
    # Create groups
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    gestionnaire_group, _ = Group.objects.get_or_create(name='Gestionnaire')
    consultant_group, _ = Group.objects.get_or_create(name='Consultant')

    # Assigning permissions to groups (placeholder, customize as needed)
    # Here, you'd add any specific model permissions if required

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_user_groups_and_permissions),
    ]
