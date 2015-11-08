from django.contrib import admin
from gameworld.models import Room, Door
from django import forms

class RoomAdminForm(forms.ModelForm):

    class Meta:
        model = Room
        exclude = []

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name',)
    form = RoomAdminForm

@admin.register(Door)
class DoorAdmin(admin.ModelAdmin):
    pass
