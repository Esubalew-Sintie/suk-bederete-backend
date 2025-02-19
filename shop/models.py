from django.db import models
from merchant.models import Merchant
from builder.models import Template
from account.models import Account
from django.apps import apps
from django.db.models import Avg
from category.models import ShopCategory
import uuid
from datetime import timedelta, datetime
from django.utils import timezone


class CustomizedTemplate(models.Model):
    original_template = models.ForeignKey(Template, on_delete=models.CASCADE)
    modifiedby = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='customized_templates', to_field='unique_id')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_template.name

class CustomizedPage(models.Model):
    customized_template = models.ForeignKey(CustomizedTemplate, related_name='pages', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    html = models.TextField()
    css = models.TextField()
    js = models.TextField()

    def __str__(self):
        return f"{self.customized_template.original_template.name} - {self.name} - {self.customized_template.modifiedby.user.email}"

class Shop(models.Model):
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ]

    name = models.CharField(max_length=200)
    owner = models.ForeignKey(Merchant, on_delete=models.CASCADE, to_field='unique_id')
    preview_image = models.ImageField(upload_to="images/preview/", blank=True, null=True)
    customized_template = models.ForeignKey(CustomizedTemplate, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=255, unique=True, blank=True, editable=False)
    category = models.ForeignKey(ShopCategory, on_delete=models.SET_NULL, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    suspense = models.BooleanField(default=False)  # Default to False initially
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='unpaid')  # Changed default to 'unpaid'
    next_payment_due_date = models.DateTimeField(null=True, blank=True)
    last_payment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.unique_id:
            # Generate the custom unique ID
            new_uuid = uuid.uuid4()
            potential_unique_id = f"{self.name}-{new_uuid}"

            # Ensure the custom ID is unique
            while Shop.objects.filter(unique_id=potential_unique_id).exists():
                new_uuid = uuid.uuid4()
                potential_unique_id = f"{self.name}-{new_uuid}"
            
            self.unique_id = potential_unique_id

        # Set the last payment date to creation date if not set
        if not self.last_payment_date:
            self.last_payment_date = self.created_date

        # Set the next payment due date to 5 minutes after the last payment date
        if not self.next_payment_due_date:
            if self.last_payment_date:
                self.next_payment_due_date = self.last_payment_date + timedelta(minutes=5)
            else:
        # Handle the case where last_payment_date is None, e.g., set a default value or raise an error
                self.next_payment_due_date = datetime.now() + timedelta(minutes=5)  # Example: set to current time + 5 minutes
        # Or you might want to raise an error or handle this case differently
        # raise ValueError("last_payment_date is None")

        # Check if the payment is due and update the status and suspense fields
        if self.next_payment_due_date and timezone.is_naive(self.next_payment_due_date):
            self.next_payment_due_date = timezone.make_aware(self.next_payment_due_date, timezone.get_current_timezone())

    # Compare timezone-aware datetimes
        if timezone.now() >= self.next_payment_due_date:
            self.status = 'unpaid'
            self.suspense = True
        else:
            self.status = 'paid'
            self.suspense = False

        super().save(*args, **kwargs)

    def make_payment(self):
        """Mark the shop as paid for the current duration and set the next payment due date."""
        self.last_payment_date = timezone.now()
        self.next_payment_due_date = self.last_payment_date + timedelta(minutes=5)
        self.status = 'paid'
        self.suspense = False
        self.save()

    def check_payment_status(self):
        """Check and update the payment status and suspense field dynamically."""
        if timezone.now() >= self.next_payment_due_date:
            self.status = 'unpaid'
            self.suspense = True
        else:
            self.status = 'paid'
            self.suspense = False
        self.save()
        return self.status, self.suspense
    
    def suspend(self):
        self.suspense = True
        self.save()

    def unsuspend(self):
        self.suspense = False
        self.save()

class ShopRating(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    rating = models.IntegerField()  # You can define your rating system here
    comment = models.TextField(blank=True, null=True)  # Optional comment from the user
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.shop.name} - {self.user.email} - {self.rating}"

class Screenshot(models.Model):
    image = models.ImageField(upload_to='images/screenshots/')
    caption = models.CharField(max_length=255, blank=True)

class Picture(models.Model):
    image = models.ImageField(upload_to='pictures/')
