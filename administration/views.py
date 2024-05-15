from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from accounts.models import LibraryStaff, LibraryStaffMoreInfo
from books.models import Book, BookReservation, BorrowReservedBook, Classification, BorrowBookRecords, WalkInUser
from .forms import LibraryAdminStaffLoginForm, AddLibraryStaffForm,AddBookForm, AddClassificationForm, BorrowBookForm, WalkInUserForm, AdminPasswordResetForm
from administration.decorators import unauthenticated_user,allowed_users
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.utils import timezone
from django.contrib import messages
import json
from datetime import date

from django.http import HttpResponse
from django.core.management import call_command
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
# Create your views here.

@login_required(login_url='admin_login')
@allowed_users(allowed_roles=["LIBRARY_STAFF"], allowed_position=["ADMIN"])
def admin_index(request):

    total_reservation = BookReservation.objects.filter(status="APPROVED",date_updated__date=date.today()).count()
    total_pending = BookReservation.objects.filter(status="PENDING").count()
    total_reserved_borrowed = BorrowReservedBook.objects.filter(status="BORROWED").count()
    total_borrowed_today = BorrowBookRecords.objects.filter(borrowed_date__date=date.today()).count()

    context = {
        'total_reserved' : total_reservation,
        'pending'        : total_pending,
        'borrowed'       : total_reserved_borrowed,
        'total_borrowed_today' : total_borrowed_today
    }


    return render(request,'administration/index.html',context)

@login_required(login_url='admin_login')
@allowed_users(allowed_roles=["LIBRARY_STAFF"])
def admin_addstaff(request):
    form = AddLibraryStaffForm()

    if request.method == "POST":
        form = AddLibraryStaffForm(request.POST)
        if form.is_valid():
            staff = form.save(commit=False)  # Save the form data but don't commit to the database yet
            staff.is_superuser = True        # Set is_superuser to True
            staff.save()                     # Now save to the database
            position = request.POST.get('position')
            LibraryStaffMoreInfo.objects.create(user=staff, position=position)
            messages.success(request, 'Staff account created successfully!')
            return redirect('admin_staff_list')

    context = {
        'form': form,
    }

    return render(request, 'administration/add_staff.html', context)

@login_required(login_url='admin_login')
@allowed_users(allowed_roles=["LIBRARY_STAFF"])
def admin_staff_list(request):
    staff_list = LibraryStaff.objects.all()
    context = {
        'staff_list' : staff_list
    }
    return render(request,'administration/list_of_staff.html',context)



@login_required(login_url='admin_login')
@allowed_users(allowed_roles=["LIBRARY_STAFF"], allowed_position=["ADMIN"])
def admin_add_book(request):
    form = AddBookForm()

    if request.method == "POST":
        form = AddBookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Book successfully added!")
            return redirect('admin_book_list')

    context = {
        'form' : form
    }
    
    return render(request,'administration/add_book.html',context)



@login_required(login_url='admin_login')
@allowed_users(allowed_roles=["LIBRARY_STAFF"])
def admin_add_book_classification(request):

    book_classification_list = Classification.objects.all()


    form = AddClassificationForm()

    if request.method == "POST":
        form = AddClassificationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Successfully added!")
            return redirect('admin_add_classification')

    context = {
        'form' : form,
        'classification_list' : book_classification_list,
    }
    return render(request,"administration/add_book_classification.html", context)


@login_required(login_url='admin_login')
@allowed_users(allowed_roles=["LIBRARY_STAFF"], allowed_position=["ADMIN","STAFF"])
def admin_book_list(request):
    book_list = Book.objects.all()

    context = {
        'book_list' : book_list
    }

    return render(request,'administration/book_list.html',context)


@login_required(login_url='admin_login')
@allowed_users(allowed_roles=["LIBRARY_STAFF"])
def admin_reservation_list(request):
    reservation_list = BookReservation.objects.filter(status="PENDING")
    approved_list = BookReservation.objects.filter(status="APPROVED",is_claimed=False)
    context = {
        'reservations' : reservation_list,
        'approved_list' : approved_list, 
    }

    return render(request,'administration/reservation_list.html',context)


@login_required(login_url='admin_login')
@allowed_users(allowed_roles=["LIBRARY_STAFF"])
def approve_reservation(request,pk):
    
    update_reservation = BookReservation.objects.get(id=pk)
    update_reservation.status = "APPROVED"
    update_reservation.save()
    return redirect('admin_reservation_list')

@login_required(login_url='admin_login')
@allowed_users(allowed_roles=["LIBRARY_STAFF"])
def decline_reservatioon(request,pk):
    update_reservation = BookReservation.objects.get(id=pk)
    update_reservation.status = "DECLINE"
    update_reservation.save()
    return redirect('admin_reservation_list')


"""
modified this code!
"""
@login_required(login_url='admin_login')
@allowed_users(allowed_roles=["LIBRARY_STAFF"])
def borrowed_reserved(request):
    test =  request.GET.get('param_reservation')
    reservation_select = BookReservation.objects.get(id=test)
    borrow_reservation_book = BorrowReservedBook.objects.create(reserved_book=reservation_select)
    borrow_reservation_book.save()
    reservation_select.is_claimed = True
    reservation_select.save()
    # borrow_reservation_book.save()
    return redirect('admin_reservation_list')


# @login_required(login_url='admin_login')
# @allowed_users(allowed_roles=["LIBRARY_STAFF"])
# def borrow_book_loan(request):
    
    



@login_required(login_url='admin_login')
@allowed_users(allowed_roles=["LIBRARY_STAFF"], allowed_position=["ADMIN","STAFF"])
def borrow_books(request):

    borrow_book_records =  BorrowBookRecords.objects.filter(reservation__isnull=False).order_by('-borrowed_date')
    borrow_book_records_walkin = BorrowBookRecords.objects.filter(walk_in_user__isnull=False).order_by('-borrowed_date')
    # borrowed_books = BorrowReservedBook.objects.all()

    context = {
        # 'borrowed_books' : borrowed_books,
        'borrow_records' : borrow_book_records,
        'walk_in_records' : borrow_book_records_walkin
    }

    return render(request,'administration/book_borrow.html',context)


def borrow_book_walkin(request):

    form = BorrowBookForm()
    walk_in_form = WalkInUserForm()

    

    if request.is_ajax():

        try:

        
            first_name = request.POST.get('first_name')
            
            middle_name = request.POST.get('middle_name')

            last_name = request.POST.get('last_name')

            contact =  request.POST.get('contact_number')

            item_to_leave = request.POST.get('item_to_leave')

            description = request.POST.get('description')

            date_to_return = request.POST.get('date_to_return')

            books = request.POST.get('books')

            

            book_list =  json.loads(books)

            if len(book_list)  != 0:

                walk_in = WalkInUser(first_name=first_name, middle_name=middle_name, last_name=last_name, contact_number=contact)

                walk_in.save()

                if walk_in:


                    for book in book_list:
                        
                        get_book = Book.objects.get(id=book.get('pk'))
                        borrow_book_records = BorrowBookRecords(book=get_book, walk_in_user=walk_in,  item_to_leave=item_to_leave, description=description, date_to_return=date_to_return)
                        borrow_book_records.save()
            

                    return JsonResponse({'message': 'success'})
        except BaseException as e:
            return JsonResponse({'message' : 'failed', 'error' : f'{e}'})

    context =  {
        'borrow_item_form' : form,
        'walk_in_form' : walk_in_form,
    }
    return render(request,"administration/borrow_book_walk.html", context)

def return_book(request,pk):
    book =  BorrowReservedBook.objects.get(id=pk)
    book.returned_date = timezone.now()
    book.status = "RETURNED"
    book.save()
    return redirect('book_borrow_list')


@login_required(login_url='admin_login')
@allowed_users(allowed_roles=["LIBRARY_STAFF"])
def return_books_from_reservation(request,pk):

    book_data =  BorrowBookRecords.objects.get(id=pk)

    book_data.returned_date = timezone.now()
    book_data.status = "RETURNED"

    book_data.save()
    # pass
    # book_data = BorrowBookRecords.objects.filter(reservation__qr_code__contains=qr_code)

    # print(book_data)

    return redirect('book_borrow_list')



@login_required(login_url='admin_login')
@allowed_users(allowed_roles=["LIBRARY_STAFF"], allowed_position=["ADMIN","STAFF"])
def scan_qr_page(request):
    return render(request,"administration/scan_book.html")

@login_required(login_url='admin_login')
@allowed_users(allowed_roles=["LIBRARY_STAFF"], allowed_position=["ADMIN","STAFF"])
def get_borrow_info_book(request,qr):

    form = BorrowBookForm()

    reservation_data = BookReservation.objects.filter(qr_code=qr)
    context = {
        "reservations" : reservation_data,
        "form" : form
    }

    # for reser in reservation_data:
    #     print(reser.is_claimed)



    if request.method == "POST":
        item_to_leave = request.POST.get('item_to_leave')
        description = request.POST.get('description')
        date_to_return = request.POST.get('date_to_return')

        for reserve in reservation_data:
            # print(reserve.is_claimed)
            reserve.is_claimed = True
            reserve.save()
            # print(reserve.id)
            borrow_book_add =  BorrowBookRecords.objects.create(reservation=reserve,item_to_leave=item_to_leave, description=description, date_to_return=date_to_return)
            borrow_book_add.save()


        
        return redirect('book_borrow_list')


    return render(request,'administration/borrow_info_book.html',context)


@login_required(login_url='admin_login')
@allowed_users(allowed_roles=["LIBRARY_STAFF"], allowed_position=["ADMIN","STAFF"])
def search_qr(request):

    if request.is_ajax():
        res = None
        qr =  request.POST.get('qr',None)
        data = []

        reservation = BookReservation.objects.filter(qr_code__icontains=qr,is_claimed=False,status="APPROVED")


        if len(reservation) > 0 and len(qr) > 0:
            # print(len(reservation))
            for item  in reservation:
                items = {
                    'pk' : item.pk,
                    'book' : item.book.title,
                    'reservee' : item.reservee.get_full_name(),
                    'reservation_date' : item.date_reservation.strftime("%b %d, %Y"),
                    'status' : item.status,
                }
                data.append(items.copy())
            res =  data
        else:
            res =  "No resevation found"

        return JsonResponse({'data' : res})
    return JsonResponse({})

def admin_login(request):
    form = LibraryAdminStaffLoginForm(request.POST or None)

    if request.POST and form.is_valid():
        user = form.login(request)
        if user is not None:
            login(request, user)
            if user.type == "LIBRARY_STAFF":
                return redirect('admin_index')
            else:
                print("sorry you are not authorize to access the administration")
    
    context = {
        'form' : form
    }

    return render(request,'administration/admin_login.html',context)

def admin_logout(request):
    logout(request)
    return redirect('admin_login')






def get_book_info_walk(request):
    
    search_book = request.GET.get('search')

    res = None

    payload = []

    # if request.is_ajax():

    if search_book:
        book_objects =  Book.objects.filter(title__icontains=search_book)

        for book in book_objects:
            items = {
            'pk' : book.pk,
            'title' : book.title,
            'author' : book.author,
            'edition' : book.edition
            }
            payload.append(items.copy())
        res =  payload
    else:
        res = "No book in our record"

    return JsonResponse({'status' : 200,'books' : res})


    # return JsonResponse({})

def get_book_borrowed(request):
    
    search_book = request.GET.get('book_borrow_list')

    res = None

    payload = []

    # if request.is_ajax():

    if search_book:
        book_objects =  Book.objects.filter(title__icontains=search_book)

        for book in book_objects:
            items = {
            'pk' : book.pk,
            'title' : book.title,
            'author' : book.author,
            'edition' : book.edition
            }
            payload.append(items.copy())
        res =  payload
    else:
        res = "No book in our record"

    return JsonResponse({'status' : 200,'books' : res})


    # return JsonResponse({})

# @login_required
@login_required(login_url='admin_login')
@allowed_users(allowed_roles=["LIBRARY_STAFF"], allowed_position=["ADMIN","STAFF"])
def account_settings(request):

    form = PasswordChangeForm(request.user)

    if request.method == "POST":
        form  = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            
            user =  form.save()

            # print(user)
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')


    context = {
        'form_password' : form
    }
    return render(request, 'administration/settings.html',context)




def borrowed_books_list(request):
    # Query to get records where status is 'BORROWED'
    borrowed_books = BorrowReservedBook.objects.filter(status=BorrowReservedBook.Status.BORROWED)
    
    context = {
        'borrowed_books': borrowed_books
    }
    
    return render(request, 'administration/borrowed_books.html', context)

def reserved_books_list(request):
    # Query to get records where status is 'BORROWED'
    borrowed_books = BookReservation.objects.filter(status=BookReservation.Status.APPROVED)
    
    context = {
        'reservations': borrowed_books
    }
    
    return render(request, 'administration/reserved_books.html', context)

def backup_restore(request):
    if request.method == 'POST':
        if 'backup' in request.POST:
            call_command('backup_db')
            return HttpResponse("Database backed up successfully.")
        elif 'restore' in request.POST:
            call_command('restore_db')
            return HttpResponse("Database restored successfully.")
    return render(request, 'administration/backup_restore.html')

# utils


def save_book_data(walk_in_id : int, book_data : list, **kwargs):


    pass


class AdminPasswordResetView(PasswordResetView):
    template_name = 'password/password_reset.html'
    success_url = reverse_lazy('admin_password_reset_done')
    # form_class = AdminPasswordResetForm
    email_template_name = 'emails/admin/admin_reset_password_email.html'
    subject_template_name = 'emails/admin/admin_password_reset_subject.txt'


class AdminPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password/password_reset_done.html'


class AdminPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "password/password_reset_confirm.html"
    success_url = reverse_lazy("admin_password_reset_complete")


class AdminPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "password/password_reset_complete.html"

