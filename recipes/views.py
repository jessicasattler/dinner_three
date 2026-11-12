from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import Recipe, Favorite


def index(request):
    """Display all recipes."""
    recipes = Recipe.objects.all()
    return render(request, 'recipes/index.html', {'recipes': recipes})


def recipe_detail(request, pk):
    """Display a single recipe."""
    recipe = get_object_or_404(Recipe, pk=pk)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists()
    
    return render(request, 'recipes/detail.html', {
        'recipe': recipe,
        'is_favorite': is_favorite
    })


@login_required
def create_recipe(request):
    """Create a new recipe."""
    if request.method == 'POST':
        Recipe.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            ingredients=request.POST.get('ingredients'),
            instructions=request.POST.get('instructions'),
            created_by=request.user
        )
        messages.success(request, 'Recipe created successfully!')
        return redirect('index')
    
    return render(request, 'recipes/form.html')


@login_required
def update_recipe(request, pk):
    """Update a recipe - explicit ownership check."""
    recipe = get_object_or_404(Recipe, pk=pk)
    
    # Explicit authorization check
    if recipe.created_by != request.user:
        messages.error(request, 'You do not have permission to edit this recipe.')
        return redirect('recipe_detail', pk=pk)
    
    if request.method == 'POST':
        recipe.title = request.POST.get('title')
        recipe.description = request.POST.get('description')
        recipe.ingredients = request.POST.get('ingredients')
        recipe.instructions = request.POST.get('instructions')
        recipe.save()
        messages.success(request, 'Recipe updated successfully!')
        return redirect('recipe_detail', pk=pk)
    
    return render(request, 'recipes/form.html', {'recipe': recipe})


@login_required
def delete_recipe(request, pk):
    """Delete a recipe - explicit ownership check."""
    recipe = get_object_or_404(Recipe, pk=pk)
    
    # Explicit authorization check
    if recipe.created_by != request.user:
        messages.error(request, 'You do not have permission to delete this recipe.')
        return redirect('recipe_detail', pk=pk)
    
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Recipe deleted successfully!')
        return redirect('index')
    
    return render(request, 'recipes/confirm_delete.html', {'recipe': recipe})


@login_required
@require_http_methods(["POST"])
def toggle_favorite(request, pk):
    """Toggle favorite status for a recipe."""
    recipe = get_object_or_404(Recipe, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    
    if not created:
        favorite.delete()
        return JsonResponse({'favorited': False})
    
    return JsonResponse({'favorited': True})


def register(request):
    """User registration."""
    if request.method == 'POST':
        from django.contrib.auth.models import User
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'recipes/register.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('index')
    
    return render(request, 'recipes/register.html')


def login_view(request):
    """User login with axes throttling."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'recipes/login.html')


def logout_view(request):
    """User logout."""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('index')


# API endpoints for DAST testing
def api_recipes(request):
    """API endpoint to list recipes."""
    recipes = Recipe.objects.values('id', 'title', 'description', 'created_by__username')
    return JsonResponse(list(recipes), safe=False)


def api_recipe_detail(request, pk):
    """API endpoint for recipe detail."""
    recipe = get_object_or_404(Recipe, pk=pk)
    return JsonResponse({
        'id': recipe.id,
        'title': recipe.title,
        'description': recipe.description,
        'ingredients': recipe.ingredients,
        'instructions': recipe.instructions,
        'created_by': recipe.created_by.username
    })
