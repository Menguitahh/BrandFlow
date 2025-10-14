from django.contrib import admin
from .models import (
    ServiceCategory, Service, Project, QuoteRequest, Payment, ProjectMessage
)

# Registrar solo los modelos de branding que realmente se usan
admin.site.register(ServiceCategory)
admin.site.register(Service)
admin.site.register(Project)
admin.site.register(QuoteRequest)
admin.site.register(Payment)
admin.site.register(ProjectMessage)