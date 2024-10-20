from django.contrib import admin

from finanace_backend.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)

admin.site.register(Location)


admin.site.register(LocationBasedExpenditure)
