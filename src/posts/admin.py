from django.contrib import admin
from .models import Post
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from klingon.admin import TranslationInline, create_translations

# Register your models here.
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title','timestamp','updated','tag','id','user']
    list_filter = ["updated",'timestamp']
    search_fields = ['title','tag']
    inlines = [TranslationInline]
    # actions = [create_translations]
    class Meta:
        model = Post
admin.site.register(Post,PostModelAdmin)

from django.contrib.sessions.models import Session
class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
admin.site.register(Session, SessionAdmin)




class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('id',)}),
    )


# admin.site.register(User, MyUserAdmin)