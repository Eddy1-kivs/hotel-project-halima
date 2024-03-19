from django.shortcuts import render, redirect
from django.views import View
import json
import datetime
import pytz
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading
from django.contrib.auth.decorators import login_required
from .models import Meal
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Meal, CartItem, Rooms, Order
from django.db.models import Sum

# Create your views here.
 
 
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail-silently == False)


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'email already in use'}, status=409)
        return JsonResponse({'email': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should be alphanumeric'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'username already in use'}, status=409)
        return JsonResponse({'username': True})

 
class RegistrationView(View):
    def get(self, request):
        return render(request, 'Auth/register.html')

    def post(self, request):
        # Get the User data
        # validate
        # create a new User
        # messages.success(request, 'success whatsapp')

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'Auth/register.html', context)

                user = User.objects.create_user(username=username, email=email, password=password)
                user.set_password(password)
                user.is_active = False
                user.save()
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64': uidb64,
                                                   'token': token_generator.make_token(user)})

                activate_url = 'http://'+domain+link

                email_body = 'Hi '+user.username + 'Please use this link to verify your account\n' + activate_url

                email_subject = 'Activate your account'
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@semycolon.com',
                    [email],
                )
                email.send()
                messages.success(request, 'Your Registration form was received. Kindly check your email to '
                                          'verify your account')
        return render(request, 'Auth/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('login'+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request, 'Account has been activated successfully')
            return redirect('login')
        except Exception as ex:
            pass

        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'Auth/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome '+user.username + ', You are now logged in')
                    return redirect('shop')
                messages.error(request, 'Account is not activated')
                return render(request, 'auth/login.html')
            messages.error(request, 'Invalid email or password')
            return render(request, 'Auth/login.html')
        messages.error(request, 'login')
        return render(request, 'Auth/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')
    
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def dining(request):
    meals = Meal.objects.all()

    context = {
        'meals': meals
    }

    return render(request, 'Dining.html', context)

def blog(request):
    return render(request, 'blog.html')

def contact(request):
    return render(request, 'contact.html')

def login(request):
    return render(request, 'Auth/login.html')

def register(request):
    return render(request, 'Auth/register.html')
  
def accomodation(request):
    rooms = Rooms.objects.all()
    context = {
        'rooms': rooms
    }
    return render(request, 'accomodation.html', context)

def view_room(request, room_id):
    room = Rooms.objects.get(id=room_id)
    return render(request, 'rooms_view.html', {'room': room})

def view_meal(request, meal_id):
    meal = Meal.objects.get(id=meal_id)
    return render(request, 'view_meal.html', {'meal': meal})

@login_required(login_url='/login')
def shop(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_amount = sum(cart_item.quantity * cart_item.meal.price for cart_item in cart_items)
    return render(request, 'shop.html', {'cart_items': cart_items, 'total_amount': total_amount})


@login_required(login_url='/login')
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required(login_url='/login')
def add_to_cart(request, meal_id):
    if request.method == 'POST':
        meal = get_object_or_404(Meal, id=meal_id)
        if meal:
            cart_item, created = CartItem.objects.get_or_create(user=request.user, meal=meal)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            messages.success(request, f"{meal.name} added to cart successfully.")
            return redirect('view_meal', meal_id=meal_id)
    return redirect('shop') 
 
@login_required(login_url='/login')
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    if request.method == 'POST':
        cart_item.delete()
        return redirect('shop')
    return redirect('shop')

@login_required(login_url='/login')
def remove_all_from_cart(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        cart_items.delete()
        return redirect('shop')
    return redirect('shop') 
 
@login_required(login_url='/login')
def increment_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('shop')

@login_required(login_url='/login')
def decrement_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('shop')

@login_required(login_url='/login')
def create_order(request):
    if request.method == 'POST':
        # Extract order details from the form submission
        user = request.user
        meal_id = request.POST.get('meal_id')
        quantity = request.POST.get('quantity')
        delivery_location = request.POST.get('delivery_location')
        payment_mode = request.POST.get('payment_mode')

        # Fetch the meal object if it exists
        meal = get_object_or_404(Meal, id=meal_id)

        # Validate quantity
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity must be a positive integer.")
        except ValueError:
            messages.error(request, "Invalid quantity.")
            return redirect('create_order')

        # Calculate subtotal
        subtotal = meal.price * quantity

        # Create the order
        Order.objects.create(
            user=user,
            meal=meal,
            quantity=quantity,
            subtotal=subtotal,
            delivery_location=delivery_location,
            payment_mode=payment_mode
        )

        # Show success message
        messages.success(request, 'Your order has been placed successfully!')

        # Redirect to a success page or any other page as needed
        return redirect('order_success')  # Assuming you have a URL named 'order_success'

    # If the request method is not POST, render the order.html template
    return render(request, 'order.html')
