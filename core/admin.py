from django.contrib import admin
from .models import ConsultationRequest


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'preferred_car', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'preferred_car')
    list_filter = ('created_at',)
