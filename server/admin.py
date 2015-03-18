from django.contrib import admin
from server.models import *

# Register your models here.

admin.site.register(Server)
#admin.site.register(Member)
admin.site.register(Volunteer)

class MemberAdmin(admin.ModelAdmin):
    pass

admin.site.register(Member,MemberAdmin)
