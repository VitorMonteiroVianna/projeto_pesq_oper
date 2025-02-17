"""
URL configuration for app project.

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
from resource_optimization.views import OptimizationProcessAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('process/', OptimizationProcessAPIView.as_view(), name='create_process'),
    path('process/<uuid:process_id>/', OptimizationProcessAPIView.as_view(), name='get_process'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login (gera JWT)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Atualiza o token
]
