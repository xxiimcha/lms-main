from django import forms
from django.forms import formset_factory
from books.models import BookReservation



class DateInput(forms.DateInput):
    input_type = 'date'

class BookReservationForm(forms.ModelForm):
    
    # book = forms.Op(label="Select Book to reserve")
    
    class Meta:
        model = BookReservation

        fields = [
            'book',
            # 'date_reservation'
        ]  

        # exclude = ('reservee','date_reservation','status','is_claimed','date_created','date_updated',)

ReservationFormset  = formset_factory(BookReservationForm, extra=1,)

# ReservationFormset = modelformset_factory(BookReservation,form=BookReservationForm,extra=0)
