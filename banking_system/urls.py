from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('auth/', include('auth_app.urls')),
    path('transaction/', include('transaction_app.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls)
]
