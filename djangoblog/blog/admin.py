from django.contrib import admin
from .models import Post

# Register your models here.


class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_date', 'author']
    list_display_links = ['created_date']
    list_editable = ['title']
    list_filter = ['created_date']
    search_fields = ['title']

    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)
