from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Nominee, Vote

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('election_id',)}),
    )

admin.site.register(CustomUser)
admin.site.register(Nominee)
admin.site.register(Vote)
