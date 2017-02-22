from django.contrib import admin
from register.models import User


class UserAdmin(admin.ModelAdmin):
    fields = ['user_email', 'user_team_name', 'user_real_name', 'user_af1', 'user_af2', 'user_paid']
    list_display = ['user_email', 'user_team_name', 'user_real_name', 'user_af1', 'user_af2', 'user_paid']
    list_editable = ['user_paid']
    list_filter = ['user_paid']
    list_per_page = 1000
    ordering = ('user_email',)


# Register your models here.
admin.site.register(User, UserAdmin)
