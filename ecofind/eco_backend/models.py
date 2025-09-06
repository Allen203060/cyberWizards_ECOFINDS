from django.db import models
 
from django.contrib.auth.models import AbstractUser

# It's good practice to have a custom user model from the start
class User(AbstractUser):
    """
    Custom user model to allow for future profile extensions.
    """
    email = models.EmailField(unique=True)
    # Add other profile fields here later, e.g., profile_picture, bio

    def _str_(self):
        return self.username

class Category(models.Model):
    """
    Model for product categories.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(' ', '-')
        super(Category, self).save(*args, **kwargs)

    def _str_(self):
        return self.name

class Product(models.Model):
    """
    Model for a single product listing.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Using a CharField for the placeholder as requested.
    # For a real implementation, you would use models.ImageField
    image_placeholder = models.URLField(max_length=500, blank=True, null=True, default="https://placehold.co/600x400/EEE/31343C?text=EcoFinds")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_sold = models.BooleanField(default=False)

    def _str_(self):
        return self.title

class CartItem(models.Model):
    """
    Represents an item in a user's cart.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def _str_(self):
        return f"{self.quantity} of {self.product.title} for {self.user.username}"

class Order(models.Model):
    """
    Model for a completed purchase/order, for the "Previous Purchase" view.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Order {self.id} by {self.user.username}"