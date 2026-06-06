from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from .models import Film, Kategoria, Ulubione, HistoriaOgladania, Komentarz, Ocena, Profil
from .forms import RegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm, KomentarzForm, OcenaForm

def index(request):
    query = request.GET.get('q')
    if query:
        filmy = Film.objects.filter(
            Q(tytul__icontains=query) | Q(gatunek__icontains=query)
        ).distinct()
    else:
        filmy = Film.objects.all()

    najnowsze = Film.objects.order_by('-data_dodania')[:5]
    return render(request, 'movies/index.html', {
        'filmy': filmy,
        'najnowsze': najnowsze,
        'query': query,
        'kategorie': Kategoria.objects.all()
    })

def movie_detail(request, pk):
    film = get_object_or_404(Film, pk=pk)
    oceny = film.oceny.all()
    komentarze = film.komentarze.all().order_by('-data_dodania')

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Ulubione.objects.filter(uzytkownik=request.user, film=film).exists()

    # Inicjalizacja formularzy (dla GET)
    ocena_form = OcenaForm()
    komentarz_form = KomentarzForm()

    if request.user.is_authenticated:
        # Wstępne wypełnienie pola oceny, jeśli użytkownik już ocenił
        try:
            ocena_uzytkownika = Ocena.objects.get(film=film, uzytkownik=request.user)
            ocena_form = OcenaForm(initial={'ocena': ocena_uzytkownika.ocena})
        except Ocena.DoesNotExist:
            pass

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Musisz być zalogowany.')
            return redirect('login')

        # Sprawdzamy, który formularz został wysłany
        if 'submit_ocena' in request.POST:
            ocena_form = OcenaForm(request.POST)
            if ocena_form.is_valid():
                Ocena.objects.update_or_create(
                    film=film,
                    uzytkownik=request.user,
                    defaults={'ocena': ocena_form.cleaned_data['ocena']}
                )
                messages.success(request, 'Ocena zapisana.')
                return redirect('movie_detail', pk=film.pk)
            else:
                # Formularz oceny niepoprawny – zostawiamy komentarz_form pusty
                komentarz_form = KomentarzForm()
                # Odtwarzamy pole oceny, aby nie stracić wprowadzonej wartości (opcjonalnie)
                # Dzięki temu błędy zostaną wyświetlone
        elif 'submit_komentarz' in request.POST:
            komentarz_form = KomentarzForm(request.POST)
            if komentarz_form.is_valid():
                Komentarz.objects.create(
                    film=film,
                    autor=request.user,
                    tresc=komentarz_form.cleaned_data['tresc']
                )
                messages.success(request, 'Komentarz dodany.')
                return redirect('movie_detail', pk=film.pk)
            else:
                # W przypadku błędu w komentarzu odtwarzamy poprzedni stan oceny
                if request.user.is_authenticated:
                    try:
                        ocena_uzytkownika = Ocena.objects.get(film=film, uzytkownik=request.user)
                        ocena_form = OcenaForm(initial={'ocena': ocena_uzytkownika.ocena})
                    except Ocena.DoesNotExist:
                        ocena_form = OcenaForm()

    # Zapis do historii oglądania (przy każdym wejściu na stronę)
    if request.user.is_authenticated:
        HistoriaOgladania.objects.get_or_create(
            uzytkownik=request.user,
            film=film,
            defaults={'data_obejrzenia': timezone.now()}
        )

    return render(request, 'movies/movie_detail.html', {
        'film': film,
        'oceny': oceny,
        'komentarze': komentarze,
        'ocena_form': ocena_form,
        'komentarz_form': komentarz_form,
        'is_favorite': is_favorite,
    })

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profil.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Konto utworzone. Jesteś zalogowany.')
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'movies/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Zalogowano pomyślnie.')
                return redirect('index')
            else:
                messages.error(request, 'Nieprawidłowa nazwa użytkownika lub hasło.')
    else:
        form = LoginForm()
    return render(request, 'movies/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile_view(request):
    profil, created = Profil.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profil)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profil zaktualizowany.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profil)
    return render(request, 'movies/profile.html', {'u_form': u_form, 'p_form': p_form})

@login_required
def toggle_favorite(request, pk):
    film = get_object_or_404(Film, pk=pk)
    fav, created = Ulubione.objects.get_or_create(uzytkownik=request.user, film=film)
    if not created:
        fav.delete()
        messages.info(request, 'Usunięto z ulubionych.')
    else:
        messages.success(request, 'Dodano do ulubionych.')
    return redirect('movie_detail', pk=pk)

@login_required
def favorites_list(request):
    fav = Ulubione.objects.filter(uzytkownik=request.user).select_related('film')
    return render(request, 'movies/favorites.html', {'favorites': fav})

@login_required
def history_list(request):
    history = HistoriaOgladania.objects.filter(uzytkownik=request.user).select_related('film')
    return render(request, 'movies/history.html', {'history': history})

@login_required
def delete_comment(request, pk):
    komentarz = get_object_or_404(Komentarz, pk=pk, autor=request.user)
    film_pk = komentarz.film.pk
    komentarz.delete()
    messages.info(request, 'Komentarz usunięty.')
    return redirect('movie_detail', pk=film_pk)