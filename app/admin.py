from django.contrib import admin
import xlwt
from django.http import HttpResponse
from .models import Meal, CartItem, Room, Order, BookedRoom, Message, Income, ProfitLoss, Expense
from django.utils import formats

def export_income_data(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="income_data.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Income Data')

    # Write headers
    row_num = 0
    columns = ['Date', 'Food Income', 'Accommodation Income', 'Total']
    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title)

    # Write data
    for obj in queryset:
        row_num += 1
        row = [
            formats.date_format(obj.date, "SHORT_DATE_FORMAT"),
            obj.food_income,
            obj.accommodation_income,
            obj.total
        ]
        for col_num, cell_value in enumerate(row):
            ws.write(row_num, col_num, cell_value)

    wb.save(response)
    return response

export_income_data.short_description = "Export Selected Incomes to Excel"

def export_profit_loss_data(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="profit_loss_data.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Profit Loss Data')

    # Write headers
    row_num = 0
    columns = ['Date', 'Profit', 'Loss']
    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title)

    # Write data
    for obj in queryset:
        row_num += 1
        row = [
            formats.date_format(obj.date, "SHORT_DATE_FORMAT"),  # Format the date
            obj.profit,
            obj.loss
        ]
        for col_num, cell_value in enumerate(row):
            ws.write(row_num, col_num, cell_value)

    wb.save(response)
    return response

export_profit_loss_data.short_description = "Export Selected Profit Loss to Excel"

def export_expense_data(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="expense_data.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expense Data')

    # Write headers
    row_num = 0
    columns = ['Date', 'Food Expenses', 'Housing Expenses', 'Total']
    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title)

    # Write data
    for obj in queryset:
        row_num += 1
        row = [
            formats.date_format(obj.date, "SHORT_DATE_FORMAT"),  # Format the date
            obj.food_expenses,
            obj.housing_expenses,
            obj.total
        ]
        for col_num, cell_value in enumerate(row):
            ws.write(row_num, col_num, cell_value)

    wb.save(response)
    return response

export_expense_data.short_description = "Export Selected Expenses to Excel"


class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'beds', 'description')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal', 'quantity', 'delivery_location', 'paid', 'phone_number') 

class BookedRoomAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'date_of_reporting', 'date_of_exit', 'guests', 'payment_mode', 'phone_number', 'paid', 'price')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'message')

class IncomeAdmin(admin.ModelAdmin):
    list_display = ('date', 'food_income', 'accommodation_income', 'total')
    actions = [export_income_data]

class ProfitLossAdmin(admin.ModelAdmin):
    list_display = ('date', 'profit', 'loss')
    actions = [export_profit_loss_data]

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'food_expenses', 'housing_expenses', 'total')
    actions = [export_expense_data]

admin.site.register(Meal, MealAdmin)
admin.site.register(CartItem)
admin.site.register(Room, RoomAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(BookedRoom, BookedRoomAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(ProfitLoss, ProfitLossAdmin)
admin.site.register(Expense, ExpenseAdmin)
