from django.contrib import admin
from server.models import *
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

# Register your models here.

admin.site.register(Server)
#admin.site.register(Member)
admin.site.register(Volunteer)

class MemberAdmin(admin.ModelAdmin):
    pass

admin.site.register(Member,MemberAdmin)
