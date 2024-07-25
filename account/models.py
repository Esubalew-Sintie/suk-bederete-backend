from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models.signals import post_save
from django.dispatch import receiver
from merchant.models import Merchant
from customer.models import Customer
class MyaccountManager(BaseUserManager):
    use_in_migrations = True
    REQUIRED_FIELDS = []
    
    def _create_user(self, email, password, role, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, role=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, role, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self._create_user(email, password, 'admin', **extra_fields)

class Account(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('merchant', 'Merchant'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(max_length=50, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MyaccountManager()

    def generate_tokens(self):
        refresh = RefreshToken.for_user(self)
        access_token = refresh.access_token
        return {
            'refresh': str(refresh),
            'access': str(access_token),
        }

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, add_label):
        return True
    
# @receiver(post_save, sender=Account)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         if instance.role == 'merchant' and not Merchant.objects.filter(user=instance).exists():
#             Merchant.objects.create(user=instance)
#         elif instance.role == 'customer' and not Customer.objects.filter(user=instance).exists():
#             Customer.objects.create(user=instance)
# # @receiver(post_save, sender=Account)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         if instance.role == 'merchant':
#             Merchant.objects.create(user=instance)
#         elif instance.role == 'customer' and not Customer.objects.filter(user=instance).exists():
#             Customer.objects.create(user=instance)
# # @receiver(post_save, sender=Account)
# # def create_user_profile(sender, instance, created, **kwargs):
# #     if created:
# #         if instance.role == 'merchant':
# #             Merchant.objects.create(user=instance)
# #         elif instance.role == 'client':
# #             Customer.objects.create(user=instance)
