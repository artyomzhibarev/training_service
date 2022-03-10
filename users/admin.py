from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', )
    search_fields = ('id', 'email', )
    ordering = ('date_joined', )
