from django.contrib import admin

from .models import Author, Category, Post, Comment, PostView, ContactUs

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(ContactUs)

admin.site.site_header = "Unrevelling Destination"
admin.site.site_title = "Unrevelling Destination"
admin.site.index_title = "Admin Panel for Unrevelling Destination"
