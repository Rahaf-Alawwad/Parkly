from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User


class CustomAdmin(UserAdmin):
    list_display = ('username', 'first_name','last_name','email','user_type', 'last_login')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login' , 'user_type')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, CustomAdmin)
