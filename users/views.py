from django.shortcuts import render
from .forms import NewUserCreationForm, UpdateUser, NewKeyword
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success, error
from django.shortcuts import redirect, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Profiles,Keywords
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.core.paginator import Paginator


def registered(request):
    page = {
        'header': 'Dziękujemy za rejestrację!',
        'title': 'Rejestracja',
             }
    return render(request,'users/registered.html')


def register(request):
    form = NewUserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('../registered/')
    page = {'header': 'ZAPRASZAMY DO REJESTRACJI',
                'title': 'Rejestracja',
                }
    return render(request, 'users/register.html', {'form':form, 'page':page} )


#aktualizacja ustawień konta
@login_required
def profile_settings(request):
    page = {'header': 'Ustawienia konta'}
    try:
        if request.method == 'POST':
            form = UpdateUser(request.POST, instance=request.user)
            form.is_valid()
            form.save()
            success(request, 'Twoje konto zostało zaktualizowane')
            return redirect('profile_settings')
#domyślnie, tj. przed przesłaniem formularza, formularz wypełniony
#wartościami, które już są w bazie, aktualnymi
        else:
            form = UpdateUser()
            form.initial={'username': request.user.username,
             'email': request.user.email,}
    except ValueError:
        error(request, 'Nieprawidłowa wartość.')
        return redirect('profile_settings')
    return render(request, 'users/profile_settings.html', {'page':page, 'form':form})


@login_required
def profile_legal(request):
    page = {'header':'Informacje prawne'}
    return render(request, 'users/profile_legal.html', {'page':page})

#logowanie
class UserLoginView(LoginView):
    model = User
    fields = ['username', 'password']

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['username'].label = 'nazwa użytkownika'
        form.fields['password'].label = 'hasło'
        return form


#Wyświetlanie istniejących profili // ClassBasedView
class ProfileListView(LoginRequiredMixin, ListView):
    model = Profiles
    template_name = 'users/profile.html'
    paginate_by = 9


    def get_queryset(self):
        # userprofiles = super().get_queryset()
        username = self.request.user
        userprofiles = Profiles.objects.filter(user_id=username)
        return userprofiles


    def get_context_data(self, **kwargs):
        context = super(ProfileListView, self).get_context_data(**kwargs)
        # liczy ilość profili zalogowanego użytkownika
        #jeżeli nie ma żadnego, to na zachętę wyświetla przykładowy.
        sum = Profiles.objects.filter(user_id=self.request.user).count()
        context['page'] = {'header': 'Twoje profile', 'title':'profile', 'sum':sum}
        return context

#tworzenie nowego profilu   //class based view
class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profiles
    template_name = 'users/new_profile.html'
    fields = ['name', 'description']

    # podajemy usera jako foreign key dla tego modelu //tabeli z db
    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)


#wyświetlanie szczegółów profilu
class ProfileDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Profiles
    template_name = 'users/profile_detail.html'
    paginate_by = 12

    def test_func(self):
        profile = self.get_object()
        if self.request.user == profile.user_id:
            return True
        else:
            return False;

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        # liczy ilość słów kluczowych profilu
        #jeżeli nie ma żadnego, to na zachętę wyświetla przykład.
        keywords = Keywords.objects.filter(id_profile= self.object)
        sum = len(keywords)
        context['page'] = {'sum':sum, 'keywords':keywords}
        return context



#edycja profilu
class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profiles
    template_name = 'users/new_profile.html'
    fields = ['name', 'description']

    def test_func(self):
        profile = self.get_object()
        if self.request.user == profile.user_id:
            return True
        else: return False;

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['name'].label = 'nazwa'
        form.fields['description'].label = 'opis'
        return form

    # podajemy usera jako foreign key dla tego modelu //tabeli z db
    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)


#usuwanie profilu
class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profiles
    template_name = 'users/profile_delete.html'

    def test_func(self):
        profile = self.get_object()
        if self.request.user == profile.user_id:
            return True
        else: return False;

    def test_func(self):
        profile = self.get_object()
        if self.request.user == profile.user_id:
            return True
        else: return False;

    def get_success_url(self):
        return reverse('profile')


#dodawanie keywords
@login_required
def newKeyword(request, id_profile):
    context = {}
    context['id_profile'] = id_profile
    #test czy na pewno do odpowiedniego profilu dodajemy
    profile = Profiles.objects.filter(id_profile=id_profile).values()
    if request.user.pk != profile[0]['user_id_id']:
        raise PermissionDenied
    form = NewKeyword(request.POST or None)
    if request.method == 'POST':
        form.is_valid()
        obj = form.save(commit=False)
        obj.save()
        obj.id_profile.add(context['id_profile'])
        obj.save()
        success(request, 'Powstało nowe słowo kluczowe')
        return redirect('profile_detail', context['id_profile'])
        # return redirect(f"/users/profile_detail/{context['id_profile']}")
    return render(request, 'users/new_keyword.html', {'form': form})


#update keywords
class KeywordUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Keywords
    template_name = 'users/new_keyword.html'
    fields = ['name']

    #test sprawdza, czy słowo które chcemy modyfikować jest w profilach użytkownika
    def test_func(self):
        ProfilesforUser = Profiles.objects.values_list('id_profile',flat=True).filter(user_id=self.request.user)
        for profile in ProfilesforUser:
            profile_keywords=Keywords.objects.values_list('id_keyword', flat=True).filter(id_profile=profile)
            if self.kwargs['pk'] in profile_keywords:
                return True
        return False;

    def get_success_url(self):
        id_profile = Keywords.id_profile.through.objects.filter(keywords_id=self.object.pk).values()[0]['profiles_id']
        return reverse('profile_detail', kwargs={'pk':id_profile})

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['name'].label = ''
        return form


#usuwanie słowa kluczowego
class KeywordDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Keywords
    template_name = 'users/keyword_delete.html'

    def test_func(self):
        ProfilesforUser = Profiles.objects.values_list('id_profile', flat=True).filter(user_id=self.request.user)
        for profile in ProfilesforUser:
            profile_keywords = Keywords.objects.values_list('id_keyword', flat=True).filter(id_profile=profile)
            if self.kwargs['pk'] in profile_keywords:
                return True
        return False;

    def get_success_url(self):
        id_profile = Keywords.id_profile.through.objects.filter(keywords_id=self.object.pk).values()[0]['profiles_id']
        return reverse('profile_detail', kwargs={'pk': id_profile})




