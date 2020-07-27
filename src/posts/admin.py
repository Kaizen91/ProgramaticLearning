from django.contrib import admin

from .models import Author, Category, Post, Comment, PostView, User

admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(PostView)
admin.site.register(User)
