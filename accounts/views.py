from django.urls import reverse_lazy
from helpers.qr_helper import qr_code_generator


from django.shortcuts import redirect, render
from django.http import HttpResponse


from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import ReaderRegistrationForm,ReaderLoginForm,ReaderEditInfoForm,ReaderMoreInfoEditForm,ReaderFormset
from books.forms import BookReservationForm,ReservationFormset
from .models import Reader, ReaderMoreInfo
from books.models import Book, BookReservation, BorrowReservedBook, BorrowBookRecords
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
# Create your views here.


from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from helpers import EmailHelper#,account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.views import PasswordResetView
import datetime

@login_required
def profile_reader(request,pk):
    # name = Reader.objects.get(id=pk)
    user_borrowed_books = BorrowReservedBook.objects.filter(reserved_book__reservee=pk,status="RETURNED")
    test_user_borrowed_books = BorrowBookRecords.objects.filter(reservation__reservee=pk, status="RETURNED")
    no_of_borrowed_returned_books =BorrowBookRecords.objects.filter(reservation__reservee=pk, status="RETURNED").count()

    context = {
        "borrowed_books" : test_user_borrowed_books,
        "total_borrowed_books" : no_of_borrowed_returned_books
    }

    return render(request,'accounts/dashboard.html',context)

@login_required
def profile_edit(request,pk):
    reader = Reader.objects.get(id=pk)
    reader_form = ReaderEditInfoForm(instance=reader)
    reader_formset = ReaderFormset(instance=reader)

    if request.method == "POST":
        reader_form = ReaderEditInfoForm(request.POST,instance=reader)
        reader_formset = ReaderFormset(request.POST,instance=reader)

        if reader_form.is_valid() and reader_formset.is_valid():
            reader_form.save()
            reader_formset.save()
            return redirect('profile',pk=request.user.id)

    context = {
        'reader_form' : reader_form,
        'reader_formset' : reader_formset,
    }
    return render(request,'accounts/edit-profile.html',context)



def reader_reservations(request):
    form =  BookReservationForm()
    reservation_pending_list = BookReservation.objects.filter(reservee=request.user,status="PENDING")
    reservation_approved_list = BookReservation.objects.filter(reservee=request.user,status="APPROVED",is_claimed=False)

    if request.method == "POST":
        form = BookReservationForm(request.POST)
        if form.is_valid():
            user = request.user
            book_post = request.POST.get('book')
            book = Book.objects.get(id=book_post)
            date_reservation = request.POST.get('date_reservation')
            reservation = BookReservation.objects.create(book=book, reservee=user, date_reservation=date_reservation)
            # reservation.save()
            # form.save()
            return redirect('reservation-profile')
    context = {
        'form':form,
        'pending_reservations' : reservation_pending_list,
        'approved_reservations' : reservation_approved_list,
    }
    return render(request,'accounts/reservations.html',context)

def reader_makereservation(request,pk):
    qr_code = qr_code_generator()
    check_exists = BookReservation.objects.filter(qr_code=qr_code).exists()


    formset = ReservationFormset()

    if request.method == "POST":
        formset =  ReservationFormset(request.POST, request.FILES)
       
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    reservation = form.save(commit=False)
                    reservation.reservee = request.user
                    reservation.date_reservation = request.POST.get('date_resevation_text')
                    if check_exists:
                        print('may kapareho')
                        qr_code = qr_code_generator()
                    reservation.qr_code = qr_code
                    reservation.save()

            return redirect('reservation-profile')

    context = {
        "formset" : formset
    }

    

    return render(request,'accounts/make-reservation.html',context)


def registration_reader(request):

    if  request.user.is_authenticated: 
        return redirect('profile',pk=request.user.id)


    form = ReaderRegistrationForm()

    if request.method == "POST":
        form = ReaderRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            sex = request.POST.get('sex')
            address = request.POST.get('address')
            birth_date = request.POST.get('birth_date')
            birth_place = request.POST.get('birth_place')
            reader_type = request.POST.get('reader_type')
            school = request.POST.get('school')

            user1 = Reader.objects.get(email=request.POST.get('email'))
            reader_add_info = ReaderMoreInfo.objects.create(
                user=user1,
                sex=sex,
                address=address,
                birth_date=birth_date,
                birth_place=birth_place,
                reader_type=reader_type,
                school=school
            )



            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('accounts/activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = form.cleaned_data.get('email')

            email = EmailHelper(mail_subject,message,to_email)
            email.send_email()

            # return redirect('login')
            return HttpResponse('Please confirm your email address to complete the registration')
    context  = {
        'form' : form
    }
    return render(request,'registration/register.html',context)



def login_reader(request):
    # if request.request.user.is_authenticated:
    
    if  request.user.is_authenticated: 
        return redirect('profile',pk=request.user.id)

    form = ReaderLoginForm()

    if request.method == "POST":
        form = ReaderLoginForm(request.POST)
        if form.is_valid():
            user = form.login(request)
            if user is not None:
                login(request,user)
                return redirect('home')

    context = {
        'form' : form
    }
    return render(request,'registration/login.html',context)


def logout_reader(request):
    logout(request)
    return redirect('login')



def render_qrcode(request,qrcode):

    context = {
        'qrcode': qrcode
    }
    return render(request,'accounts/qr_render.html',context)


def activate_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Reader.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Reader.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # return
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        # return
        return HttpResponse('Activation link is invalid!')



def change_password(request):
    form = PasswordChangeForm(request.user)

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()

            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully changed!")
            return redirect("change_password_user")

        else:
            messages.error(request, "Please correct the error below")


    context = {
        'form_password' : form
    }

    return render(request, "accounts/change_password.html",context)