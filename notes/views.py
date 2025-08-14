from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import View
from django.db.models import Q
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

# Create Recipe


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'notes/recipe_create.html'
    success_url = reverse_lazy('home')
    # Return ingredients created by the user and Admin

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = RecipeIngredientFormSet(
                self.request.POST,
                form_kwargs={'user': self.request.user}
            )
        else:
            context['formset'] = RecipeIngredientFormSet(
                form_kwargs={'user': self.request.user}
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


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 12

    def get_queryset(self):
        q = (self.request.GET.get('q') or '').strip()
        qs = Recipe.objects.filter(user=self.request.user)
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

        # Order by created_at
        has_created_at = any(
            f.name == 'created_at' for f in Recipe._meta.fields)
        order_field = '-created_at' if has_created_at else '-id'
        return qs.order_by(order_field)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = (self.request.GET.get('q') or '').strip()
        return ctx


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'notes/recipe_update.html'
    model = Recipe
    fields = [
        'name',
        'description',
        'target_og', 'target_fg',
        'start_fermentation', 'end_fermentation',
        'start_coldcrash', 'end_coldcrash',
        'start_conditioning', 'end_conditioning',
        'brewing_notes', 'testing_notes',
        'verdict',
    ]
    success_url = reverse_lazy('home')
    context_object_name = 'recipe'

    def test_func(self):
        return self.request.user == self.get_object().user


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'notes/recipe_delete.html'
    model = Recipe
    success_url = reverse_lazy('home')
    context_object_name = 'recipe'

    def test_func(self):
        return self.request.user == self.get_object().user
