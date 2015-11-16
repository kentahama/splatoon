from django.contrib import admin
from recruit.models import Room, User

class UserInline(admin.TabularInline):
    model = User
    extra = 8

class RoomAdmin(admin.ModelAdmin):
    inlines = [UserInline]

admin.site.register(Room, RoomAdmin)
