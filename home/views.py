from django.shortcuts import render
from books.models import Book
# Create your views here.


def index(request):
    return render(request,'home/index.html')


def about(request):
    return render(request,'home/about.html')


def menu(request):
    book_list = Book.objects.all()
    context = {
        'book_list' : book_list
    }
    return render(request,'home/menu.html',context)


def services(request):
    return render(request,'home/services.html')