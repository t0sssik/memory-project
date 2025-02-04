"""
URL configuration for MemoryProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Main import views
from Main import validation

urlpatterns = [
    path('admin/', admin.site.urls),
    path( '', views.index, name='index'),
    path('first/', views.first, name='first'),
    path('auth/', views.auth, name='auth'),
    path('auth/validate_email/', validation.validate_email, name='validate_email'),
    path('auth/validate_login/', validation.validate_login_data, name='validate_login'),
    path('logout/', views.logout_view, name='logout'),
    path('offer/', views.offer, name='offer'),
    path('test/', views.test, name='test'),
    path('test/end', views.end, name='end'),
]
