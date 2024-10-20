from django.contrib import admin

from .models import *


# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)

admin.site.register(Location)

admin.site.register(LocationBasedExpenditure)

admin.site.register(Transaction)
admin.site.register(Expense)
