from django.contrib import admin
from .models import Expense, ExpenseCategory

# Register your models here.
admin.site.register(ExpenseCategory)
admin.site.register(Expense)