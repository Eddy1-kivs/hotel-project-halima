from django.db import models
from django.contrib.auth.models import User

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
    amount_paid = models.IntegerField()
 

    def __str__(self):
        return f"Booking for {self.room.name} by {self.user.username}"

class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return self.name
