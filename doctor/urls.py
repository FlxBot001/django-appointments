from django.urls import path
from . import views
from .views import HomeTemplateView, AppointmentTemplateView, ManageAppointmentTemplateView, StartTemplateView, register, otp_verify, user_login

urlpatterns = [
    path("register/", register, name="register"),
    path("otp-verify/", otp_verify, name="otp_verify"),
    path("login/", user_login, name="login"),

    path("", HomeTemplateView.as_view(), name="home"),
    path("start/", StartTemplateView.as_view(), name="start"),
    path("make-an-appointment/", AppointmentTemplateView.as_view(), name="appointment"),
    path("manage-appointments/", ManageAppointmentTemplateView.as_view(), name="manage"),
    path("register/", views.register, name="register"),
    path("otp-verify/", views.otp_verify, name="otp_verify"),
    path("login/", views.user_login, name="login"),
    path('profile/', views.profile_list, name='profile_list'),
    path('appointment/', views.appointment_list, name='appointment_list'),
]
