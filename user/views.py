from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from django.contrib.auth.models import User
from user.models import *
from django.shortcuts import render, Http404
from django.shortcuts import get_object_or_404
from  agaclar.models import *

# Create your views here.
def giris(request):
    username = ''
    password1 = ''
    password2 = ''
    if request.method == 'POST':
        if 'register' in request.POST:
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2'] 
            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Bu kullanici adi kullaniliyor.')
                elif len(password1)<8:
                    messages.error(request, 'Parola en az 8 karakter olmali.')
                else:
                    user = User.objects.create_user(username = username, password=password1)
                    user.save()
                    messages.success(request, 'Basariyla kayit oldunuz.')
                    return redirect('index')
            else:
                messages.error(request, 'Parolalar eslesmiyor.')                
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username , password=password )

        if user is not None:
            login(request, user)
            messages.success(request, 'Giris Yapildi')
            return redirect('index')
        else:
            messages.info(request, 'Kullanici Adi veya Sifre Hatali')
            return redirect ('login')
    else:
        return render(request, 'login.html')    


def cikis(request):
    logout(request)
    messages.success(request, 'Cikis Yapildi')
    return render(request, 'index.html')

def profile(request, profile_id):
    # Arisarge kullanıcısının profilini al
    arisarge_profile = Profile.objects.filter(user__username='admin').first()

    # Eğer profil Arisarge'ye aitse, giriş yapılmamış olsa bile bu profili gösterebiliriz
    if arisarge_profile and arisarge_profile.id == profile_id:
        profile = arisarge_profile
    else:
        # Diğer profiller için giriş yapmış olmalı
        profile = get_object_or_404(Profile, id=profile_id)
        if not request.user.is_authenticated:
            return redirect('login')  # Giriş yapılmamış kullanıcıları giriş sayfasına yönlendir

    # Profille ilişkilendirilen arazileri al
    arsalar = Arazi.objects.filter(arsasahibi=profile)

    context = {
        'profile': profile,
        'arsalar': arsalar,
    }
    return render(request, 'profil.html', context)





def medya(request):

    return render(request, 'profil/medya.html')   