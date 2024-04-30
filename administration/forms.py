from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate
from accounts.models import LibraryStaff, LibraryStaffMoreInfo
from books.models import Book, Classification, BorrowBookRecords, WalkInUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth.forms import PasswordResetForm


class DateInput(forms.DateInput):
    input_type = 'date'

class LibraryAdminStaffLoginForm(forms.Form):
    username = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={
                                   'class' : 'form-control form-control-user',
                                   'placeholder':'Enter Email Address'
                               }),
                               required=True             
                                            )

    password = forms.CharField(max_length=50,
                               widget=forms.PasswordInput(attrs={
                                   'class' : 'form-control form-control-user',
                                   'placeholder':'Password'
                               }),     
                                            )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry login was invalid. Please try again.")
        return self.cleaned_data


    def login(self,request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class AddLibraryStaffForm(UserCreationForm):

    STAFF = "STAFF"
    ADMIN = "ADMIN"


    POSITION = [
        (STAFF, "STAFF"),
        (ADMIN, "ADMIN")
    ]

    first_name = forms.CharField(max_length=50,label='Your name',
                               widget=forms.TextInput(attrs={
                                   'class' : 'form-control',
                                   'placeholder':'Enter first name'
                               })   
                                )

    middle_name = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={
                                   'class' : 'form-control',
                                   'placeholder':'Enter middle name'
                               }),
                               required=False     
                                )

    last_name = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={
                                   'class' : 'form-control',
                                   'placeholder':'Enter last name'
                               }),     
                                )


        

    email =  forms.EmailField(max_length=50,
                               widget=forms.TextInput(attrs={
                                   'class' : 'form-control',
                                   'placeholder':'Email Address'
                               }),     
                                )

    password1 = forms.CharField(max_length=50,
                               widget=forms.PasswordInput(attrs={
                                   'class' : 'form-control',
                                   'placeholder':'Password'
                               }),     
                                            )

    password2 = forms.CharField(max_length=50,
                               widget=forms.PasswordInput(attrs={
                                   'class' : 'form-control',
                                   'placeholder':'Password Confirmation'
                               }),     
                                            )
                                            
    # department = forms.CharField(max_length=50,
    #                            widget=forms.TextInput(attrs={
    #                                'class' : 'form-control',
    #                                'placeholder':'Select Department'
    #                            }),     
    #                             )

    position = forms.ChoiceField(choices=POSITION,
                            #    widget=forms.Select(attrs={
                            #        'class' : 'form-control',
                            #        'placeholder':'Select Position'
                            #    }),     
                                )
    
    date_hired = forms.DateField(widget=DateInput, required=True, label="Date Hired")

    birth_date = forms.DateField(widget=DateInput, required=True, label="Birth Date")
    birth_place = forms.CharField(max_length=100, label="Birth Place")
    class Meta:
        model = LibraryStaff

        fields = [
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'password1',
            'password2',
            'position',
            'date_hired', 
            'birth_date',
            'birth_place'
        ]

class AddLibraryStaffMoreInfoForm(forms.ModelForm):

    department = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={
                                   'class' : 'form-control',
                                   'placeholder':'Select Department'
                               }),     
                                )

    position = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={
                                   'class' : 'form-control',
                                   'placeholder':'Select Position'
                               }),     
                                )
    class Meta:
        model = LibraryStaffMoreInfo
        fields = [
            'department',
            'position'
        ]

LibraryStaffFormset = inlineformset_factory(LibraryStaff,LibraryStaffMoreInfo,fields=('position',),can_delete=False)




class AddBookForm(forms.ModelForm):

    class Meta:
        model = Book
        exclude = ('created_at','updated_at',)

class AddClassificationForm(forms.ModelForm):

    class Meta:
        model = Classification
        fields = "__all__"



class BorrowBookForm(forms.Form):

    def __init__(self, form_type = None, *args, **kwargs )-> None:
        self.type = form_type
        # self.field_order = ['item_to_leave','description','borrowed_date']
        super().__init__(*args,**kwargs)
        
        if self.type is not None:
            self.fields['borrowed_date']=  forms.DateField(widget=DateInput, required=True)
        # super().__init__()


    ID = "ID"
    LICENSE = "LICENSE"
    OTHERS = "OTHERS"


    ITEMS = [
        (ID, "ID"),
        (LICENSE, "LICENSE"),
        (OTHERS, "OTHERS")
    ]

    
    
    item_to_leave = forms.ChoiceField(choices=ITEMS,
                                    label='Item to Leave (ID, License Card or others)',
                                    widget=forms.Select(attrs={
                                    'class' : 'form-select',
                                    'placeholder' : 'Select Item'
                                    },),
                                        
                                    )
    description = forms.CharField(widget=forms.Textarea(attrs={
                                "rows":"4",
                                "class" :"form-control"
                                }),
                                required=False,
                                label='Description',)


    date_to_return = forms.DateField(widget=DateInput, required=True, label="Date to return the book")



    class Meta:
        model = BorrowBookRecords


      
        
        fields = [
            'item_to_leave',
            'description',
            'date_to_return',
        ]
    # item to leave
    # description

class WalkInUserForm(forms.ModelForm):
    

    class Meta:
        model =  WalkInUser

        fields = [
            'first_name',
            'middle_name',
            'last_name',
            'contact_number'
        ]


class AdminPasswordResetForm(PasswordResetForm):

    user_type = forms.CharField(widget=forms.HiddenInput(), initial='admin')