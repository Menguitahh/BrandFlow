from django.db import models
from django.utils import timezone
from user_control.models import Users
from django.core.validators import MinValueValidator


# ==== Branding Models ====

class ServiceCategory(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    service_type = models.CharField(max_length=100, default='general')
    base_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    features = models.JSONField(default=dict, blank=True)
    delivery_time = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ('quote', 'Quote'),
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
        ('payment_pending', 'Payment Pending'),
        ('in_progress', 'In Progress'),
        ('review', 'Review'),
        ('pending_completion_confirmation', 'Pending Completion Confirmation'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('on_hold', 'On Hold'),
    ]

    title = models.CharField(max_length=200)
    brief = models.TextField(blank=True)
    status = models.CharField(max_length=35, choices=STATUS_CHOICES, default='quote')
    priority = models.CharField(max_length=30, default='normal')
    start_date = models.DateField(null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    client = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='projects')
    assigned_to = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_projects')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.status})"


class QuoteRequest(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    client = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='quote_requests')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='quote_requests')
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_by = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_quotes')
    approved_at = models.DateTimeField(null=True, blank=True)
    rejected_reason = models.TextField(null=True, blank=True)
    linked_project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='from_quote')

    def __str__(self):
        return f"Quote {self.id} - {self.title} ({self.status})"


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_simulated = models.BooleanField(default=True)
    cardholder_name = models.CharField(max_length=150, blank=True)
    card_last4 = models.CharField(max_length=4, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.project_id} - {self.status}"


class ProjectMessage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='project_messages')
    message = models.TextField()
    attachment = models.FileField(upload_to='project_messages/', blank=True, null=True)
    attachment_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_internal = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Msg {self.id} on {self.project_id} by {self.sender_id}"
    
    @property
    def has_attachment(self):
        return bool(self.attachment)
    
    @property
    def attachment_type(self):
        if not self.attachment:
            return None
        
        file_extension = self.attachment.name.split('.')[-1].lower()
        if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
            return 'image'
        elif file_extension == 'pdf':
            return 'pdf'
        else:
            return 'file'
