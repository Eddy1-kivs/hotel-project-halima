from django.contrib import admin
from .models import Meal, CartItem, Rooms


class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')

class RoomsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'beds', 'description')

admin.site.register(Meal, MealAdmin)
admin.site.register(CartItem)
admin.site.register(Rooms,RoomsAdmin)
