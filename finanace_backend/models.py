from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum


class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    ROLE_CHOICES = [
        ('student', 'Student'),
        ('employee', 'Employee'),
    ]

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        blank=True,
        null=True
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


class UserProfile(models.Model):
    PREFERENCE_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    LOCATION_CHOICES = [
        ('hyderabad', 'Hyderabad'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField(auto_now=True)

    location = models.CharField(max_length=150, choices=LOCATION_CHOICES,
                                default='hyderabad')
    preference = models.CharField(max_length=6, choices=PREFERENCE_CHOICES)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class LocationEnum(Enum):
    ALWAL = "Alwal"
    AMBERPET = "Amberpet"
    AMEERPET = "Ameerpet"
    ATTAPUR = "Attapur"
    BACHUPALLY = "Bachupally"
    BANJARA_HILLS = "Banjara Hills"
    BEGUMPET = "Begumpet"
    CHARMINAR = "Charminar"
    DILSUKHNAGAR = "Dilsukhnagar"
    ECIL = "ECIL"
    GACHIBOWLI = "Gachibowli"
    HAFIZ_BABA_NAGAR = "Hafiz Baba Nagar"
    HAYATH_NAGAR = "Hayath Nagar"
    HIMAYATNAGAR = "Himayatnagar"
    JEEDIMETLA = "Jeedimetla"
    JNTU = "JNTU"
    KARKHANA = "Karkhana"
    KOMPALLY = "Kompally"
    KONDAPUR = "Kondapur"
    KUKATPALLY = "Kukatpally"
    LB_NAGAR = "LB Nagar"
    MADHAPUR = "Madhapur"
    MALAKPET = "Malakpet"
    MANIKONDA = "Manikonda"
    MASAB_TANK = "Masab Tank"
    MEDCHAL_ROAD = "Medchal Road"
    MIYAPUR = "Miyapur"
    MOKILA = "Mokila"
    MOOSAPET = "Moosapet"
    NAGOLE = "Nagole"
    NARAYANGUDA = "Narayanguda"
    NIZAMPET = "Nizampet"
    PATANCHERU = "Patancheru"
    PEERZADIGUDA = "Peerzadiguda"
    Q_CITY = "Q City"
    SAINIKPURI = "Sainikpuri"
    SANGAREDDY = "Sangareddy"
    SAROOR_NAGAR = "Saroor Nagar"
    SERILINGAMPALLY = "Serilingampally"
    SHAMSHABAD = "Shamshabad"
    SIVARAMPALLI = "Sivarampalli"
    SURARAM = "Suraram"
    TARNAKA = "Tarnaka"
    TOLI_CHOWKI = "Toli Chowki"
    UPPAL = "Uppal"
    VANASTHALIPURAM = "Vanasthalipuram"

    @classmethod
    def choices(cls):
        return [(item.name, item.value) for item in cls]


class Location(models.Model):
    name = models.CharField(
        max_length=50,
        choices=LocationEnum.choices(),
        unique=True
    )

    def __str__(self):
        return self.get_name_display()


class Category(Enum):
    FOOD = "Food"
    ENTERTAINMENT = "Entertainment"
    TRAVEL = "Travel"
    HEALTH = "Health"
    MISCELLANEOUS = "Miscellaneous"
    RENT = "Rent"
    SAVINGS = "Savings"
    SHOPPING = "Shopping"

    @classmethod
    def choices(cls):
        return [(item.name, item.value) for item in cls]


class LocationBasedExpenditure(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=Category.choices())
    gender = models.CharField(max_length=1, choices=User.GENDER_CHOICES)

    high_percentage = models.FloatField()
    medium_percentage = models.FloatField()
    low_percentage = models.FloatField()

    class Meta:
        unique_together = ('location', 'category', 'gender')

    def __str__(self):
        return f"{self.location.name} - {self.get_category_display()} - {self.gender}"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=Category.choices())
    description = models.TextField(blank=True, null=True)
    expense_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.category}: {self.amount}"

    class Meta:
        ordering = ['-date']


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=(
        ('income', 'Income'), ('expense', 'Expense')))
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_expenses_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user} - {self.transaction_type} - {self.amount}"
