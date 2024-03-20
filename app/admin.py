from django.contrib import admin
from .models import Meal, CartItem, Room, Order, BookedRoom


class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'beds', 'description')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal', 'quantity', 'delivery_location', 'paid', 'phone_number') 

class BookedRoomAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'date_of_reporting', 'date_of_exit', 'guests', 'payment_mode', 'phone_number', 'paid', 'price')

admin.site.register(Meal, MealAdmin)
admin.site.register(CartItem)
admin.site.register(Room, RoomAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(BookedRoom, BookedRoomAdmin)
