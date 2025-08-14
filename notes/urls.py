from django.urls import path
from .views import home, profile
from django.shortcuts import redirect
from .views import RecipeCreateView, RecipeListView, RecipeUpdateView, RecipeDeleteView
from allauth.socialaccount.providers.google.views import oauth2_login


def google_login_redirect(request):
    return redirect('socialaccount_login', provider='google')


urlpatterns = [
    path('', home, name='home'),
    path('recipe/create/', RecipeCreateView.as_view(), name='create_recipe'),
    path('recipes/', RecipeListView.as_view(), name='list_recipe'),
    path('recipe/<int:pk>/update/',
         RecipeUpdateView.as_view(), name='update_recipe'),
    path('recipe/<int:pk>/delete/',
         RecipeDeleteView.as_view(), name='delete_recipe'),
    path("accounts/login/", google_login_redirect),
    path('account/profile/', profile, name='profile'),

]
