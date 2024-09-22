from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
Account = get_user_model()

class ExpenseCategory(models.Model):
    category_name = models.CharField(max_length=75)
    user = models.ForeignKey(
        Account, related_name="user_expense_category", on_delete=models.CASCADE
    )
    def __str__(self):
        return self.category_name

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey(ExpenseCategory, related_name="expense", on_delete=models.CASCADE)
    user = models.ForeignKey(Account, related_name="user_expense", on_delete=models.CASCADE)
    expense_date = models.DateTimeField()
    notes = models.TextField()
    

