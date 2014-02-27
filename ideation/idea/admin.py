from django.contrib import admin
from django import forms
from models import *


class IdeaTypeAdmin(admin.ModelAdmin):
    list_display = ('name','ordering',)
    list_editable = ('name','ordering',)

admin.site.register(IdeaType, IdeaTypeAdmin)
admin.site.register(IdeaImage)
admin.site.register(IdeaLink)
admin.site.register(Idea)