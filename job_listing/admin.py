from django.contrib import admin

# Register your models here.
from .models import JobPosting
from .import forms

admin.site.register(JobPosting)