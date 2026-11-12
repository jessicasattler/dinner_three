from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipes/create/', views.create_recipe, name='create_recipe'),
    path('recipes/<int:pk>/update/', views.update_recipe, name='update_recipe'),
    path('recipes/<int:pk>/delete/', views.delete_recipe, name='delete_recipe'),
    path('recipes/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    
    # API endpoints
    path('api/recipes/', views.api_recipes, name='api_recipes'),
    path('api/recipes/<int:pk>/', views.api_recipe_detail, name='api_recipe_detail'),
]
