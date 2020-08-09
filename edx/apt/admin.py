from django.contrib import admin
from .models import *
# Register your models here.





from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.site_header='Education'

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(AttendanceModel)
admin.site.register(ExamNumberModel)









admin.site.register(SignupModel)
admin.site.register(Subject)
admin.site.register(Topics)
admin.site.register(Question)
admin.site.register(TestGiven)
admin.site.register(Assignments)
admin.site.register(ContactModel)
