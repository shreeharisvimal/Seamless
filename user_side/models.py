from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from products.models import ProductVariant


class CustomNewManager(BaseUserManager):

    def create_superuser(self, email, username, password,phone_number, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if not email:
            raise ValueError(_('The Email field must be set'))
        if extra_fields.get('is_staff') is not True:
            raise ValueError('you are not a staff to be superuser')
        user = self.create_user(email,username,password,phone_number,**extra_fields)
        return user
    
    def create_user(self, username, email, password=None, phone_number=None, **extra_fields):
        if not email:
            raise ValueError('need email to create a user')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone_number= phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), max_length=250, unique=True)
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    start_time = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    
    new_manager = CustomNewManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phone_number']

    def __str__(self):
        return self.username
    


class Wishlist(models.Model):
    my_user = models.ForeignKey(NewUser, on_delete=models.CASCADE, null=True)
    wish_item = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f"{self.my_user} - {self.wish_item}"

