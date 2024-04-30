from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from accounts.managers import CustomUserManager
# import datetime

# Create your models here.




class User(AbstractUser):
    

    class Types(models.TextChoices):
        READER = "READER","Reader" #Student, Other-> 
        LIBRARY_STAFF = "LIBRARY_STAFF","Library Staff" # OIC, Staff->

    default_type = Types.READER

    username = None
    profile_picture = models.ImageField(upload_to='account/profile_pictures/', null=True, blank=True)
    middle_name = models.CharField(verbose_name="middle_name",max_length=50,null=True, blank=True)

    type =  models.CharField(max_length=50, choices=Types.choices, default=default_type)

    email = models.EmailField(verbose_name="email", unique=True)

    created_at = models.DateTimeField(editable=False, default=None)
    updated_at = models.DateTimeField(default=None)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type =  self.default_type
            self.created_at =  timezone.now()
        self.updated_at = timezone.now()
        return super(User,self).save(*args, **kwargs)

    def __str__(self):
        return self.email
    


class ReaderManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.READER)

    def normalize_email(self,email):
        email_parts = email.split('@')
        email_parts[-1] = email_parts[-1].lower()
        return '@'.join(email_parts)


class LibraryStaffManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.LIBRARY_STAFF)

    def normalize_email(self,email):
        email_parts = email.split('@')
        email_parts[-1] = email_parts[-1].lower()
        return '@'.join(email_parts)


class ReaderMoreInfo(models.Model):
    MALE = 'MALE'
    FEMALE = 'FEMALE'

    STUDENT = 'STUDENT'
    OTHER = 'OTHER'

    SEX = [
        (MALE, _('MALE')),
        (FEMALE, _('FEMALE'))
    ]

    READER_TYPE =[
        (STUDENT, _('STUDENT')),
        (OTHER, _('OTHER'))
    ]

    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    # middle_name = models.CharField(verbose_name="middle name",max_length=20, null=True)
    sex =  models.CharField(max_length=20, null=True,choices=SEX, verbose_name="Sex")
    address = models.TextField(verbose_name="Address")
    birth_date = models.DateField(auto_now=False, blank=True,verbose_name="Birth Date")
    birth_place = models.TextField(verbose_name="Birthplace")
    reader_type = models.CharField(max_length=20,null=True,verbose_name="Reader Type")
    school = models.TextField(verbose_name="School",default="")


    def __str__(self):
        return str(self.user)



class Reader(User):
    default_type = User.Types.READER
    objects = ReaderManager()

    class Meta:
        proxy = True

    @property
    def more(self):
        return self.readermoreinfo




class LibraryStaffMoreInfo(models.Model):

    STAFF = "STAFF"
    ADMIN = "ADMIN"


    POSITION = [
        (STAFF, "STAFF"),
        (ADMIN, "ADMIN")
    ]

    
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    # department = models.CharField(max_length=100,null=True, verbose_name="Department")
    position = models.CharField(max_length=100,null=True,verbose_name="Position",choices=POSITION)
    date_hired = models.DateField(auto_now=False, blank=True, default=None,null=True,  verbose_name="Date Hired")
    birth_date = models.DateField(auto_now=False, blank=True, default=None, null=True,verbose_name="Birth Date")
    birth_place = models.TextField(verbose_name="Birthplace", default=None, null=True)

    def __str__(self):
        return str(self.user)




class LibraryStaff(User):
    default_type = User.Types.LIBRARY_STAFF
    objects = LibraryStaffManager()
    class Meta:
        proxy =True

    @property
    def more(self):
        return self.librarystaffmoreinfo
