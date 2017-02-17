from django.contrib import admin
from home.models import Blog

class BlogAdmin(admin.ModelAdmin):
    fields = ['entry_subject', 'entry_body']
    list_display = ['entry_subject', 'entry_date']
    list_per_page = 1000
    ordering = ('-entry_date',)


admin.site.register(Blog, BlogAdmin)
