from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse, HttpResponseForbidden, \
    HttpResponseNotAllowed
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, renderers
from darmankade.models import *
from django.db.models import Q
from darmankade import forms
from rest_framework.settings import api_settings
from darmankade.forms import *
from .dao import load_doctor, load_patient
from django.contrib.auth import authenticate, login, logout

# import darmankade.views.permissions as mypermissions
# import jwt
import hashlib
from enum import Enum

from rest_framework.exceptions import APIException


class ServiceUnavailable(APIException):
    status_code = 403
    default_detail = 'you do not have access to this page'
    default_code = 'forbidden'


class IndexView(APIView):
    def get(self, request):
        context = {
        }
        return render(request, 'darmankade/index.html', context)


class DoctorRegisterView(APIView):

    def get(self, request):
        doctor_register_form = DoctorRegisterForm()
        context = {
            'doctor_register_form': doctor_register_form
        }
        return render(request, 'darmankade/doctor-register.html', context)

    def post(self, request, format=None):
        data = request.data

        username = data.get("username")
        password = data.get("password")
        mobile = data.get("mobile")
        name = data.get("name")
        spec = data.get("spec")
        number = data.get("number")
        online_pay = data.get("online_pay")
        if online_pay:
            online_pay = True
        else:
            online_pay = False

        experience_years = data.get("experience_years")
        address = data.get("address")
        phone = data.get("phone")

        w0 = data.get("w0")
        w1 = data.get("w1")
        w2 = data.get("w2")
        w3 = data.get("w3")
        w4 = data.get("w4")
        w5 = data.get("w5")
        w6 = data.get("w6")

        week_days = [
            True if w0 else False,
            True if w1 else False,
            True if w2 else False,
            True if w3 else False,
            True if w4 else False,
            True if w5 else False,
            True if w6 else False,
        ]

        doctor = Doctor(username=username, name=name, spec=spec, number=number, online_pay=online_pay,
                        experience_years=experience_years, address=address,
                        phone=phone, week_days=week_days)
        doctor.save()
        AuthProfile.objects.create_user(username=username, role='doctor', mobile=mobile, password=password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('darmankade:doctor_profile', kwargs={'pk': user.username}) + "")
        else:
            raise Http404("user does not exists")


class DoctorLoginView(APIView):

    def get(self, request):
        return render(request, 'darmankade/doctor-login.html')

    def post(self, request, format=None):
        data = request.data
        username = data.get("username")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('darmankade:doctor_profile', kwargs={'pk': user.username}) + "")
        else:
            raise Http404("user does not exists")


class PatientRegisterView(APIView):

    def get(self, request):
        patient_register_form = PatientRegisterForm()
        context = {
            'patient_register_form': patient_register_form
        }
        return render(request, 'darmankade/patient-register.html', context)

    def post(self, request, format=None):
        data = request.data
        username = data.get("username")
        password = data.get("password")
        name = data.get("name")
        mobile = data.get("mobile")

        patient = Patient(username=username, name=name)
        patient.save()
        AuthProfile.objects.create_user(username=username, role='patient', mobile=mobile, password=password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('darmankade:patient_profile', kwargs={'pk': user.username}) + "")
        else:
            raise Http404("user does not exists")


class PatientLoginView(APIView):

    def get(self, request):
        return render(request, 'darmankade/patient-login.html')

    def post(self, request, format=None):
        data = request.data
        username = data.get("username")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('darmankade:patient_profile', kwargs={'pk': user.username}) + "")
        else:
            raise Http404("user does not exists")


class DoctorProfileView(APIView):
    def get(self, request, pk, format=None):
        current_user = request.user
        if current_user.username != pk:
            return HttpResponseForbidden()
        doctor = load_doctor(pk)
        doctor_profile_form = DoctorProfileForm(instance=doctor)
        week_days = ['checked' if w else '' for w in doctor.week_days]
        context = {
            'doctor_profile_form': doctor_profile_form,
            'id': pk,
            'week_days': week_days
        }
        return render(request, 'darmankade/doctor-profile.html', context)

    def post(self, request, pk, format=None):  # a method for edit
        current_user = request.user
        if current_user.username != pk:
            return HttpResponseForbidden()

        data = request.data
        name = data.get("name")
        spec = data.get("spec")
        number = data.get("number")
        online_pay = data.get("online_pay")
        if online_pay:
            online_pay = True
        else:
            online_pay = False

        experience_years = data.get("experience_years")
        address = data.get("address")
        phone = data.get("phone")

        w0 = data.get("w0")
        w1 = data.get("w1")
        w2 = data.get("w2")
        w3 = data.get("w3")
        w4 = data.get("w4")
        w5 = data.get("w5")
        w6 = data.get("w6")

        week_days = [
            True if w0 else False,
            True if w1 else False,
            True if w2 else False,
            True if w3 else False,
            True if w4 else False,
            True if w5 else False,
            True if w6 else False,
        ]

        doctor = load_doctor(pk)
        doctor.name = name
        doctor.spec = spec
        doctor.number = number
        doctor.online_pay = online_pay
        doctor.experience_years = experience_years
        doctor.address = address
        doctor.phone = phone
        doctor.week_days = week_days
        doctor.save()

        return redirect('darmankade:doctor_profile', pk=pk)


class DoctorsView(APIView):
    def get(self, request):
        context = {
        }
        return render(request, 'darmankade/doctors.html', context)


class DoctorView(APIView):
    def get(self, request, pk, format=None):
        context = {
            'id': pk
        }
        return render(request, 'darmankade/doctor.html', context)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('darmankade:doctor_profile', pk=username)

        else:
            return HttpResponse('Unauthorized', status=401)


class PatientProfileView(APIView):
    def get(self, request, pk, format=None):
        current_user = request.user
        if current_user.username != pk:
            return HttpResponseForbidden()

        patient = load_patient(pk)
        patient_profile_form = PatientProfileForm(instance=patient)
        context = {
            'patient_profile_form': patient_profile_form,
            'id': pk,
        }

        return render(request, 'darmankade/patient-profile.html', context)

    def post(self, request, pk, format=None):  # a method for edit

        current_user = request.user
        if current_user.username != pk:
            return HttpResponseForbidden()

        data = request.data
        name = data.get("name")
        patient = load_patient(pk)
        patient.name = name
        patient.save()

        return redirect('darmankade:patient_profile', pk=pk)


class LoginAsView(APIView):
    def get(self, request):
        context = {
        }
        return render(request, 'darmankade/login-as.html', context)


class RegisterAsView(APIView):
    def get(self, request):
        context = {
        }
        return render(request, 'darmankade/register-as.html', context)


def logout_view(request):
    logout(request)
    return redirect(reverse('darmankade:index'))
