from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, DoctorDepartment, Appointment, RateModel



class AccountAdmin(UserAdmin):
    list_display =('email', 'firstname','lastname','username','date_joined','last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_files = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class DoctorAdmin(UserAdmin):
    list_display =( )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class AppAdmin(UserAdmin):
    list_display =()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)

admin.site.register(DoctorDepartment)
admin.site.register(RateModel)
admin.site.register(Appointment)