from django.contrib import admin
from .models import Kategoria, Film, Ocena, Komentarz, Ulubione, HistoriaOgladania, Profil

@admin.register(Kategoria)
class KategoriaAdmin(admin.ModelAdmin):
    list_display = ('nazwa',)

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('tytul', 'rok_produkcji', 'gatunek', 'data_dodania')
    list_filter = ('kategorie', 'gatunek')
    search_fields = ('tytul', 'opis')

admin.site.register(Ocena)
admin.site.register(Komentarz)
admin.site.register(Ulubione)
admin.site.register(HistoriaOgladania)
admin.site.register(Profil)