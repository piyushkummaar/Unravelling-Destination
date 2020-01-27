from django.contrib import admin

from .models import Author, Category, Post, ContactUs, Signup

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(ContactUs)
admin.site.register(Signup)

admin.site.site_header = "Unravelling Destination"
admin.site.site_title = "Unravelling Destination"
admin.site.index_title = "Admin Panel for Unravelling Destination"
