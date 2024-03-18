from . import views
from django.urls import path
from .views import RegistrationView, UsernameValidationView, EmailValidationView, \
    VerificationView, LoginView, LogoutView

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='hotel'),
    path('about/', views.about, name='about'),
    path('dining/', views.dining, name='dining'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('register', RegistrationView.as_view(), name='register'),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('accomodation/', views.accomodation, name='accomodation'),
    path('shop/', views.shop, name='shop'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_to_cart/<int:meal_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('meal/<int:meal_id>/', views.view_meal, name='view_meal'),
    path('remove-all-from-cart/', views.remove_all_from_cart, name='remove_all_from_cart'),
]
