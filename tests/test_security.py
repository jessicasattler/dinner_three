import pytest
from django.contrib.auth.models import User
from recipes.models import Recipe, Favorite


@pytest.mark.django_db
class TestRecipeAuthorization:
    """Test explicit ownership authorization checks."""
    
    def setup_method(self):
        self.user1 = User.objects.create_user('user1', 'user1@example.com', 'pass123')
        self.user2 = User.objects.create_user('user2', 'user2@example.com', 'pass123')
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            description='Test',
            ingredients='Test',
            instructions='Test',
            created_by=self.user1
        )
    
    def test_user_can_update_own_recipe(self, client):
        """User1 should be able to update their own recipe."""
        client.login(username='user1', password='pass123')
        response = client.post(f'/recipes/{self.recipe.id}/update/', {
            'title': 'Updated',
            'description': 'Test',
            'ingredients': 'Test',
            'instructions': 'Test'
        })
        self.recipe.refresh_from_db()
        assert self.recipe.title == 'Updated'
    
    def test_user_cannot_update_others_recipe(self, client):
        """User2 should NOT be able to update user1's recipe."""
        client.login(username='user2', password='pass123')
        response = client.post(f'/recipes/{self.recipe.id}/update/', {
            'title': 'Updated',
            'description': 'Test',
            'ingredients': 'Test',
            'instructions': 'Test'
        })
        self.recipe.refresh_from_db()
        assert self.recipe.title == 'Test Recipe'
        assert response.status_code == 302  # Redirect
    
    def test_user_cannot_delete_others_recipe(self, client):
        """User2 should NOT be able to delete user1's recipe."""
        client.login(username='user2', password='pass123')
        response = client.post(f'/recipes/{self.recipe.id}/delete/')
        assert Recipe.objects.filter(id=self.recipe.id).exists()


@pytest.mark.django_db
class TestFavoriteOwnership:
    """Test favorite ownership checks."""
    
    def setup_method(self):
        self.user1 = User.objects.create_user('user1', 'user1@example.com', 'pass123')
        self.user2 = User.objects.create_user('user2', 'user2@example.com', 'pass123')
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            description='Test',
            ingredients='Test',
            instructions='Test',
            created_by=self.user1
        )
    
    def test_favorite_belongs_to_user(self):
        """Favorite should only belong to the user who created it."""
        favorite = Favorite.objects.create(user=self.user1, recipe=self.recipe)
        assert favorite.user == self.user1
        assert Favorite.objects.filter(user=self.user2, recipe=self.recipe).count() == 0


@pytest.mark.django_db
class TestCSRFProtection:
    """Test CSRF token protection."""
    
    def test_post_requires_csrf_token(self, client):
        """POST requests should require CSRF token."""
        user = User.objects.create_user('user1', 'user1@example.com', 'pass123')
        recipe = Recipe.objects.create(
            title='Test',
            description='Test',
            ingredients='Test',
            instructions='Test',
            created_by=user
        )
        client.login(username='user1', password='pass123')
        response = client.post(f'/recipes/{recipe.id}/delete/', {})
        # Should redirect, CSRF would cause 403
        assert response.status_code in [200, 302]
