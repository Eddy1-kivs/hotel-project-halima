from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone

class Meal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='meal_images/')

    def __str__(self):
        return self.name
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.meal.price 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.meal.name} for {self.user.username}"
    
class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    beds = models.IntegerField()
    cover_image = models.ImageField(upload_to='meal_images/')
    image1 = models.ImageField(upload_to='meal_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='meal_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='meal_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='meal_images/', blank=True, null=True)


    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal = models.CharField(max_length=50)
    quantity = models.CharField(max_length=50, default= '1')
    subtotal = models.CharField(max_length=50, default= '1')
    delivery_location = models.CharField(max_length=100)
    payment_mode = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20 ,default= '254')
    paid = models.BooleanField(default=False)

    
    def __str__(self):
        return self.meal

class BookedRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_of_reporting = models.DateField()
    date_of_exit = models.DateField()
    guests = models.IntegerField()
    payment_mode = models.CharField(max_length=50, choices=[('mpesa', 'Mpesa'), ('pay_on_arrival', 'Pay on Arrival')])
    phone_number = models.CharField(max_length=20)
    paid = models.BooleanField(default=False)
    price = models.IntegerField()
 

    def __str__(self):
        return f"Booking for {self.room.name} by {self.user.username}"

class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return self.name

class Income(models.Model):
    date = models.DateField(default=timezone.now) 
    food_income = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    accommodation_income = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0) 

    def calculate_income(self):
        total_food_income = Order.objects.aggregate(total=Sum('subtotal'))['total']
        total_accommodation_income = BookedRoom.objects.aggregate(total=Sum('price'))['total']

        self.food_income = total_food_income or 0
        self.accommodation_income = total_accommodation_income or 0
        self.total = self.food_income + self.accommodation_income

    def save(self, *args, **kwargs):
        self.calculate_income()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Income - Food: {self.food_income}, Accommodation: {self.accommodation_income}, Total: {self.total}"

class ProfitLoss(models.Model):
    date = models.DateField(default=timezone.now)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    loss = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @classmethod
    def calculate_profit_loss(cls):
        # Get the start and end datetime for the previous day
        end_date = timezone.now().date()
        start_date = end_date - timezone.timedelta(days=1)

        # Get the total income for the previous day
        total_income = Income.objects.filter(date__range=(start_date, end_date)).aggregate(total=Sum('total'))['total'] or 0

        # Get the total expenses for the previous day (if any)
        # You may need to define the Expense model and its relationship with Income
        total_expenses = 0  # You need to implement this based on your Expense model

        # Calculate profit and loss
        total_profit_loss = total_income - total_expenses
        if total_profit_loss >= 0:
            cls.profit = total_profit_loss
            cls.loss = 0
        else:
            cls.profit = 0
            cls.loss = abs(total_profit_loss)

    def save(self, *args, **kwargs):
        self.calculate_profit_loss()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Profit/Loss for {self.date}: Profit - {self.profit}, Loss - {self.loss}"
