from django.contrib import admin
from .models import User, Reader, LibraryStaff
# Register your models here.
admin.site.register(User)
admin.site.register(Reader)
admin.site.register(LibraryStaff)