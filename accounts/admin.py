from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import User
from django.contrib.auth.models import Group


admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(ModelAdmin):
    fields = ('username', 'password', 'first_name', 'last_name', 'is_verified', 'is_superuser', 'is_staff', 'is_active', 'last_login', 'date_joined', 'groups', 'user_permissions')
    readonly_fields = ('password', )

@admin.register(Group)
class GroupAdmin(ModelAdmin):
    pass
