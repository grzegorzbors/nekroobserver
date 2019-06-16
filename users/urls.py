#############################################
#URLS FOR APP USERS
#############################################

from django.urls import path, include
from . import views as users_view
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('register/', users_view.register,name='register_page'),
    path('registered/',users_view.registered, name = 'registered'),
    path('login/',users_view.UserLoginView.as_view(template_name='users/login.html'), name = 'login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'), name = 'logout'),
    path('profile/', users_view.ProfileListView.as_view(), name = 'profile'),
    path('profile_settings/',users_view.profile_settings, name = 'profile_settings'),
    path('profile_legal/',users_view.profile_legal, name = 'profile_legal'),
    path('new_profile/', users_view.ProfileCreateView.as_view(), name = 'new_profile'),
    path('profile_detail/<int:pk>/', users_view.ProfileDetailView.as_view(), name = 'profile_detail'),
    path('profile_update/<int:pk>/',users_view.ProfileUpdateView.as_view(), name='profile_update'),
    path('profile_delete/<int:pk>/',users_view.ProfileDeleteView.as_view(), name ='profile_delete'),
    path('new_keyword/<int:id_profile>/', users_view.newKeyword, name = 'new_keyword'),
    path('keyword_update/<int:pk>/',users_view.KeywordUpdateView.as_view(), name='keyword_update'),
    path('keyword_delete/<int:pk>/', users_view.KeywordDeleteView.as_view(), name='keyword_delete'),

]