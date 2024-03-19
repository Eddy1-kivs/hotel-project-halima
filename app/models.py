from django.db import models
from django.contrib.auth.models import User

class Meal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='meal_images/')

    def __str__(self):
        return self.name
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Add the subtotal field

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.meal.price  # Calculate the subtotal before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.meal.name} for {self.user.username}"
    
class Rooms(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
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
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_location = models.CharField(max_length=100)
    payment_mode = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        # Calculate subtotal based on quantity and meal price
        self.subtotal = self.quantity * self.meal.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order for {self.quantity} x {self.meal.name} by {self.user.username}"
