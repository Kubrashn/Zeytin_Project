from user.models import Profile

def arisarge_profile(request):
    # Arisarge kullanıcısının profilini al
    arisarge_profile = Profile.objects.filter(user__username='admin').first()
    
    # Eğer profil varsa, profil id'sini döndür
    if arisarge_profile:
        return {'arisarge_profile_id': arisarge_profile.id}
    
    # Eğer profil bulunamazsa boş bir değer döndür
    return {}
