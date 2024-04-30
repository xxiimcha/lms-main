from django.contrib import admin


from .models import Book, BookReservation, BorrowReservedBook, Classification
# Register your models here.


admin.site.register(Book)
admin.site.register(BookReservation)
admin.site.register(BorrowReservedBook)
admin.site.register(Classification)