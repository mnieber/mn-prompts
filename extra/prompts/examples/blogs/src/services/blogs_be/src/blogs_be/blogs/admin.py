from django.contrib import admin

from blogs_be.blogs import models


class BlogPostInline(admin.TabularInline):
    model = models.BlogPost
    extra = 3


@admin.register(models.BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = (BlogPostInline,)
