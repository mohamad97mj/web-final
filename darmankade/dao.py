from darmankade.models import *
from django.http import Http404


def load_patient(pk):
    try:
        return Patient.objects.get(pk=pk)
    except Patient.DoesNotExist:
        raise Http404


def load_doctor(pk):
    try:
        return Doctor.objects.get(pk=pk)
    except Doctor.DoesNotExist:
        raise Http404
