from django.contrib import admin
from .models import Meal, CartItem


class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description') 

admin.site.register(Meal, MealAdmin)
admin.site.register(CartItem)
