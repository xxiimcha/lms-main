from django.db import models
from django.utils import timezone
from accounts.models import Reader
# Create your models here.



class Classification(models.Model):
    name = models.CharField(verbose_name="name",max_length=200)


    def __str__(self) -> str:
        return self.name




class Book(models.Model):
    
    title = models.CharField(verbose_name="Title",max_length=200)
    edition = models.IntegerField(verbose_name="Edition")
    author = models.CharField(verbose_name="Author",max_length=100)
    publisher = models.TextField(verbose_name="Publisher")
    copies = models.IntegerField(verbose_name="No. of Copies")
    # genre = models.CharField(verbose_name="Genre",max_length=100)
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, verbose_name="genre", null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None)


    def save(self,*args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)


    def __str__(self) -> str:
        return self.title


class BookReservation(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING","PENDING"  
        APPROVED = "APPROVED","Approved"
        DECLINED = "DECLINED","Decline"

    default_type = Status.PENDING

    book = models.ForeignKey(Book, on_delete=models.CASCADE,verbose_name="Book Name")
    reservee = models.ForeignKey(Reader,on_delete=models.CASCADE)
    date_reservation = models.DateField(auto_now_add=False, null=True, default='')
    status = models.CharField(verbose_name="status",max_length=100,default=default_type)
    is_claimed = models.BooleanField(default=False)
    qr_code = models.CharField(max_length=10,null=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default='')


    def save(self,*args, **kwargs):
        if not self.pk:
            self.date_created = timezone.now()
        self.date_updated = timezone.now()
        return super(BookReservation, self).save(*args, **kwargs)


    def __str__(self) -> str:
        return str(self.reservee)


class BorrowBook(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    user = models.ForeignKey(Reader,on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateTimeField(auto_now_add=False)
    status = models.CharField(max_length=10,verbose_name="status")


    def __str__(self) -> str:
        return str(self.user)

class BorrowReservedBook(models.Model):
    class Status(models.TextChoices):
        BORROWED = "BORROWED","Borrowed"  
        RETURNED = "RETURNED","Returned"

    default_type = Status.BORROWED


    reserved_book = models.ForeignKey(BookReservation, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(null=True)
    returned_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=20,verbose_name="status",default=default_type)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default='', null=True)


    def save(self,*args, **kwargs):
        if not self.pk:
            self.borrowed_date = timezone.now()
            self.date_created = timezone.now()
        self.date_updated = timezone.now()
        return super().save(*args, **kwargs)


    def __str__(self) -> str:
        return str(self.reserved_book.reservee)



class WalkInUser(models.Model):
    first_name =  models.CharField(max_length=50,verbose_name="First Name")
    middle_name =  models.CharField(max_length=50,verbose_name="Middle Name")
    last_name =  models.CharField(max_length=50,verbose_name="Last Name")
    contact_number = models.CharField(max_length=15, verbose_name="Contact No.")



    def __str__(self) -> str:

        return str(f"{self.first_name} {self.last_name}")


class BorrowBookRecords(models.Model):
    
    class Status(models.TextChoices):
        BORROWED = "BORROWED","Borrowed"  
        RETURNED = "RETURNED","Returned"


    class ItemToLeave(models.TextChoices):
        ID = "ID","Id"
        LICENSE = "LICENSE", "License"
        OTHERS = "OTHERS", "Others"

    default_type = Status.BORROWED
    default_item =  ItemToLeave.ID

    book =  models.ForeignKey(Book, on_delete=models.CASCADE, null=True) #if borrowed record is walk in
    walk_in_user = models.ForeignKey(WalkInUser, on_delete=models.CASCADE, null=True)#if borrowed record is walk in
    reservation = models.ForeignKey(BookReservation, on_delete=models.CASCADE, null=True)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateTimeField(auto_now_add=False, null=True)
    status = models.CharField(max_length=20,verbose_name="Status",default=default_type)
    item_to_leave = models.CharField(verbose_name="Item to leave", max_length=100, default=default_item)
    description  = models.TextField(null=True,verbose_name="Description")
    date_to_return = models.DateTimeField(null=True)
