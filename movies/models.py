from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from cloudinary.models import CloudinaryField

class Kategoria(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nazwa

class Film(models.Model):
    tytul = models.CharField(max_length=200)
    opis = models.TextField()
    rok_produkcji = models.PositiveIntegerField()
    gatunek = models.CharField(max_length=100)
    czas_trwania = models.PositiveIntegerField(help_text='Czas w minutach')
    plakat = CloudinaryField('image', null=True, blank=True)  # ZMIANA
    data_dodania = models.DateTimeField(auto_now_add=True)
    kategorie = models.ManyToManyField(Kategoria, related_name='filmy', blank=True)

    class Meta:
        ordering = ['-data_dodania']

    def __str__(self):
        return self.tytul

    def srednia_ocena(self):
        oceny = self.oceny.all()
        if oceny.exists():
            return round(oceny.aggregate(models.Avg('ocena'))['ocena__avg'], 1)
        return 0

    def liczba_glosow(self):
        return self.oceny.count()

class Ocena(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='oceny')
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    ocena = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    data_oceny = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('film', 'uzytkownik')

    def __str__(self):
        return f"{self.uzytkownik.username} - {self.film.tytul}: {self.ocena}"

class Komentarz(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='komentarze')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    tresc = models.TextField()
    data_dodania = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Komentarz {self.autor.username} do {self.film.tytul}"

class Ulubione(models.Model):
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ulubione')
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    data_dodania = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('uzytkownik', 'film')

    def __str__(self):
        return f"{self.uzytkownik.username} lubi {self.film.tytul}"

class HistoriaOgladania(models.Model):
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historia')
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    data_obejrzenia = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_obejrzenia']

    def __str__(self):
        return f"{self.uzytkownik.username} obejrzał {self.film.tytul}"

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username