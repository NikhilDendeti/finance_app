from django.db import models
from django.contrib.auth.models import AbstractUser
from finance_app.enums import *


# User Model
class User(AbstractUser):
    gender = models.CharField(
        max_length=6,
        choices=GenderChoices.list_of_values()
    )
    role = models.CharField(
        max_length=10,
        choices=RoleChoices.list_of_values()
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True
    )

    def __str__(self):
        return self.username


# UserProfile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField(auto_now=True)
    location = models.CharField(
        max_length=150,
        choices=LocationChoices.list_of_values(),
        default='HYDERABAD'
    )
    preference = models.CharField(
        max_length=6,
        choices=PreferenceChoices.list_of_values()
    )

    def __str__(self):
        return f"{self.user}'s Profile"


# Location Model
class Location(models.Model):
    name = models.CharField(
        max_length=50,
        choices=LocationEnum.list_of_values(),
    )

    def __str__(self):
        return self.name


# LocationBasedExpenditure Model
class LocationBasedExpenditure(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    category = models.CharField(
        max_length=50,
        choices=Category.list_of_values()
    )
    gender = models.CharField(
        max_length=6,
        choices=GenderChoices.list_of_values()
    )

    high_percentage = models.FloatField()
    medium_percentage = models.FloatField()
    low_percentage = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['location', 'category', 'gender'],
                                    name='unique_location_category_gender')
        ]

    def __str__(self):
        return f"{self.location.name} - {self.gender}"


# Expense Model
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(
        max_length=50,
        choices=Category.list_of_values()
    )
    description = models.TextField(blank=True, null=True)
    expense_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.category}: {self.expense_amount}"

    class Meta:
        ordering = ['-date']


# Transaction Model
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.list_of_values()
    )
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_expenses_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user} - {self.transaction_type} - {self.remaining_amount}"
