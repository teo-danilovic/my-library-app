from django.contrib import admin
from .models import Book, ReadingSession, Tag, Photo

# Register  models .
admin.site.register(Book)
admin.site.register(ReadingSession)
admin.site.register(Tag)
admin.site.register(Photo)