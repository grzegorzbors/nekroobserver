from django.db import models
# nie tworzymy modelu user tylko korzystamy z już istniejącego
from django.contrib.auth.models import User
from django.urls import reverse


# django database
# Create your models here.
# domyślnie NOT NULL

# Profiles, primary id_profile int, name carchar 45, status - Boolean
# związany z users - foriegn key
class Profiles(models.Model):
    id_profile = models.AutoField(primary_key=True)
    # jeśli usunięty zostanie user, to profil też
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=45)
    description = models.TextField(max_length=120, default=' ')

    # krótki opis isString
    def __str__(self):
        return f'{self.id_profile},{self.user_id}, {self.name}'

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'pk': str(self.id_profile)})


# słowa klucze, po nich prowadzone będzie wyszukiwanie
class Keywords(models.Model):
    id_keyword = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    # relacja many to many / specjalna cecha django
    id_profile = models.ManyToManyField(Profiles)

    # krótki opis isString
    def __str__(self):
        return f'{self.id_keyword}, {self.name}, {self.id_profile}'

    # view tworzące nowe słowo kluczowe
    def get_absolute_url(self):
        return reverse('keyword_update', kwargs={'pk': self.pk})

# brakuje jeszcze tabeli z ściąganymi/wysłanymi
