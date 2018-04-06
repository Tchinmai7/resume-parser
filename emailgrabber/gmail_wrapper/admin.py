# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import Email, Attachment, Company, PagesToWatch

class PagesInline(admin.TabularInline):
    model = PagesToWatch

class CompanyAdmin(admin.ModelAdmin):
    inlines = [
        PagesInline,
    ]

admin.site.register(Company, CompanyAdmin)

class AttachmentInline(admin.StackedInline):
    model = Attachment

class EmailAdmin(admin.ModelAdmin):
    inlines = [
        AttachmentInline,
    ]

admin.site.register(Email, EmailAdmin)