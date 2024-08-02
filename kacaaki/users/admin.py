from django.contrib import admin
from .models import User,NepaliStudent,DanceStudent,Teacher,Token,VideoUpload,OPT
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _




class UserAdmin(DjangoUserAdmin):
    model = User
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password','full_name','phone','age','gender','city','state','zip_code','country','photo','user_type','created_at','deleted_at')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',),
        }),
    )
    list_display = ('email',)
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, UserAdmin)
admin.site.register(Token)
admin.site.register(NepaliStudent)
admin.site.register(DanceStudent)
admin.site.register(Teacher)
admin.site.register(VideoUpload)
admin.site.register(OPT)