from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views import View
from .forms import RecipeForm, RecipeIngredientForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from notes.models import Ingredient, Recipe, DrinkType, RecipeIngredient
# Create your views here.

RecipeIngredientFormSet = inlineformset_factory(
    Recipe,
    RecipeIngredient,
    form=RecipeIngredientForm,
    extra=1,
    can_delete=True
)


def home(request):
    return render(request, 'notes/index.html')


def profile(request):
    return render(request, 'account/profile.html')


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'notes/recipe_create.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = RecipeIngredientFormSet(
                self.request.POST,
                form_kwargs={'user': self.request.user}  # <-- here
            )
        else:
            context['formset'] = RecipeIngredientFormSet(
                form_kwargs={'user': self.request.user}  # <-- here
            )
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))
