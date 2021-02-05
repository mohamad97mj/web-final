from django import forms
from darmankade.models import *
from django.forms import ModelForm, CharField, ValidationError, Textarea, TextInput, CheckboxInput, NumberInput, \
    CheckboxSelectMultiple


class PatientProfileForm(ModelForm):
    class Meta:
        model = Patient
        exclude = ['username']
        labels = {
            'name': "نام",
        }


class DoctorProfileForm(ModelForm):
    class Meta:
        model = Doctor
        exclude = ['username', 'week_days']
        labels = {
            'name': "نام",
            'spec': 'تخصص',
            'number': 'شماره نظام پزشکی',
            'online_pay': 'پرداخت آنلاین',
            'experience_years': 'تعداد سال های تجربه',
            'address': 'نشانی',
            'phone': 'تلفن',
        }


class DoctorRegisterForm(ModelForm):
    class Meta:
        model = Doctor
        exclude = ['username', 'week_days']
        help_texts = {
            'online_pay': 'پرداخت آنلاین'
        }
        widgets = {
            'name': TextInput(attrs={'placeholder': "نام"}),
            'spec': TextInput(attrs={'placeholder': 'تخصص'}),
            'number': NumberInput(attrs={'placeholder': 'شماره نظام پزشکی'}),
            'online_pay': CheckboxInput(attrs={'placeholder': 'پرداخت آنلاین'}),
            'experience_years': NumberInput(attrs={'placeholder': 'تعداد سال های تجربه'}),
            'address': TextInput(attrs={'placeholder': 'نشانی'}),
            'phone': TextInput(attrs={'placeholder': 'تلفن'}),
        }


class PatientRegisterForm(ModelForm):
    class Meta:
        model = Patient
        exclude = ['username']
        widgets = {
            'name': TextInput(attrs={'placeholder': "نام"}),
        }
