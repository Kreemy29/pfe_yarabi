from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('gestionnaire/dashboard/', views.gestionnaire_dashboard, name='gestionnaire_dashboard'),
    path('consultant/dashboard/', views.consultant_dashboard, name='consultant_dashboard'),
    path('import_files/', views.import_files, name='import_files'),
    path('upload/', views.import_files, name='upload'),
    path('results/', views.view_results, name='view_results'),
]
