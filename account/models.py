from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField

class AccountManager(BaseUserManager):
    def create_user(self, email, name, password=None, **kwargs):
        
        if not email:
            raise ValueError("Email is required")
        
        if not name:
            raise ValueError("Name is required")

        user = self.model(
            email=self.normalize_email(email),
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password, **kwargs):
        user = self.create_user(
            email=self.normalize_email(email),
            name = name,
            password = password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser= True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(null=False, blank=False, unique=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    phone_number = PhoneNumberField(null=True, blank=True)
    
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
         return True

    def has_module_perms(self, app_label):
        return True
    
class AccountDetails(models.Model):

    class Currency(models.TextChoices):
        USD = "usd", "USD"
        EURO = "euro", "EURO"
        GBP = "gbp", "GBP"
        NGN = "ngn", "NGN"
    user = models.OneToOneField(Account, related_name="user_details", on_delete=models.CASCADE)
    image = models.ImageField(max_length=255, upload_to="", default="")
    currency = models.CharField(max_length=75, choices=Currency.choices, default=Currency.NGN)
    # contact_number = PhoneNumberField(blank=False, null=False)
    # address = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.user.name


class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    