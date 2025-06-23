"""
URL configuration for agac_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from agaclar.views import *
from user.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('agac_index/', index, name='index'),
    path('map_detay/<uuid:arazi_id>/', map_detay, name='map_detay'), 
    path('map/', map, name='map'), 
    path('profile/<int:profile_id>/', profile, name='profile'),
    path('login/', giris, name='login'),
    path('logout/', cikis, name='logout'),
    path('medya/', medya, name='medya'),
    path('', ari_index, name='ari_index'),
    path('agac_detay/<uuid:agac_id>/', agac_detay, name='agac_detay'),
    path('agac_liste/<uuid:arazi_id>/', agac_liste, name='agac_liste'),
    path('tanıtım/', tanıtım , name='tanıtım')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

