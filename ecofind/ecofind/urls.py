from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from eco_backend import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'cart', views.CartItemViewSet, basename='cartitem')
router.register(r'orders', views.OrderViewSet, basename='order')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('eco_backend.urls')),
    
    # User Registration
    path('api/register/', views.UserCreateView.as_view(), name='register'),
    
    # JWT Token Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]