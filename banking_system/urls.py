from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    # Apps
    path('auth/', include('auth_app.urls')),
    path('transaction/', include('transaction_app.urls')),
    path('account/', include('accounts_app_account.urls')),
    path('employee/', include('employee_app.urls')),
    # API
    path('api/v1/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    # Task queues
    path('celery-progress/', include('celery_progress.urls'))
]
