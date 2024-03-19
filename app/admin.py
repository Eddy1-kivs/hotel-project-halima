from django.contrib import admin
from .models import Meal, CartItem, Room, Order


class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'beds', 'description')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal', 'quantity', 'delivery_location') 

admin.site.register(Meal, MealAdmin)
admin.site.register(CartItem)
admin.site.register(Room,RoomAdmin)
admin.site.register(Order, OrderAdmin)
