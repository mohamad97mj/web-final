from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'darmankade'

urlpatterns = [

    path('index', views.IndexView.as_view(), name='index'),

    path('login-as', views.LoginAsView.as_view(), name='login_as'),
    path('register-as', views.RegisterAsView.as_view(), name='register_as'),

    path('doctor-login', views.DoctorLoginView.as_view(), name='doctor_login'),
    path('patient-login', views.PatientLoginView.as_view(), name='patient_login'),

    path('doctor-register', views.DoctorRegisterView.as_view(), name='doctor_register'),
    path('patient-register', views.PatientRegisterView.as_view(), name='patient_register'),

    path('doctors', views.DoctorsView.as_view(), name='doctors'),
    path('doctors/<slug:pk>', views.DoctorView.as_view(), name='doctor'),

    path('doctors/<slug:pk>/profile', views.DoctorProfileView.as_view(), name='doctor_profile'),
    path('patients/<slug:pk>/profile', views.PatientProfileView.as_view(), name='patient_profile'),

    path('logout', views.logout_view, name='logout'),

    # path('ajax/get_x', views.get_x, name='get_x'),
]
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
