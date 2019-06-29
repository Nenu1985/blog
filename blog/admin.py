from django.contrib import admin
from .models import Post, Blog, NewsPost


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'publish', 'status',)
    list_filter = ('status', 'created', 'publish', )

    search_fields = ('title', 'body',)

    # auto complete slug field by title value
    prepopulated_fields = {'slug': ('title',)}

    # authors can be searched with lookup widget (lupa)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(NewsPost)
class NewPostAdmin(admin.ModelAdmin):
    list_display = ('post', 'read', 'added',)
