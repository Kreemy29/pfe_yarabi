from django.contrib import admin
from .models import ConsultantUser, GestionnaireUser, AdminUser

admin.site.register(ConsultantUser)
admin.site.register(GestionnaireUser)
admin.site.register(AdminUser)
