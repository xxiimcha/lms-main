from django import forms
from django.forms import inlineformset_factory, widgets
from django.contrib.auth import authenticate, models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import ReaderMoreInfo, User, Reader


class DateInput(forms.DateInput):
    input_type = 'date'

class ReaderRegistrationForm(UserCreationForm):
    MALE = 'MALE'
    FEMALE = 'FEMALE'

    SEX = [
        (MALE, "MALE"),
        (FEMALE, "FEMALE")
    ]

    STUDENT = 'STUDENT'
    OTHER = 'OTHER'

    READER_TYPE =[
        (STUDENT, "STUDENT"),
        (OTHER, "OTHER")
    ]
    
    photo = forms.CharField(widget=forms.HiddenInput(), required=False)  # Hidden field for image data

    first_name = forms.CharField(max_length=50)
    middle_name = forms.CharField(max_length=50,required=False)
    last_name = forms.CharField(max_length=50)
    # suffix = forms.CharField(max_length=50, required=False)
    sex = forms.ChoiceField(choices=SEX)
    address = forms.CharField(max_length=100)
    birth_date = forms.DateField(widget=DateInput)
    birth_place = forms.CharField(max_length=100)
    reader_type = forms.ChoiceField(choices=READER_TYPE,label="Type of Reader")
    school = forms.CharField(widget=forms.Textarea(attrs={'rows':'2'}),label="Name of School (for student, if not leave as blank)",required=False)


    class Meta:
        model = Reader
        fields = [
            'email', 'first_name', 'last_name', 'middle_name',
            'password1', 'password2', 'sex', 'address', 'birth_date',
            'birth_place', 'reader_type', 'school', 'photo', 
        ]


class ReaderLoginForm(forms.Form):
    username = forms.CharField(max_length=50,
                              widget=forms.TextInput(attrs={'placeholder':'Enter email address'}),
                              required=True,label="Email")
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password', 'id': 'id_password'}),
        required=True
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Sorry login was invalid. Please try again.")
        if  not user.is_active:
            raise forms.ValidationError("Verify your email first!")
        return self.cleaned_data

    def login(self,request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user



class ReaderEditInfoForm(UserChangeForm):

    password = None
    class Meta:
        model = Reader
        fields = [
            'first_name',
            'middle_name',
            'last_name',
        ]

class ReaderMoreInfoEditForm(forms.ModelForm):

    address = forms.CharField(widget=forms.Textarea(attrs={'rows':'2'}))
    class Meta:
        model =  ReaderMoreInfo
        fields = ['address']



ReaderFormset = inlineformset_factory(Reader,ReaderMoreInfo,fields=('address',),can_delete=False)