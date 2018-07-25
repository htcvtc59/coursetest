from django.contrib import admin
from .models import Account, Role


# Register your models here.

class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'createdate')
    ordering = ('-createdate',)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'createdate', 'role')
    ordering = ('-createdate',)


admin.site.register(Role, RoleAdmin)
admin.site.register(Account, AccountAdmin)
