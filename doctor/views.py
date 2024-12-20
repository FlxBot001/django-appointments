from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.utils.timezone import now, timedelta
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.core.mail import EmailMessage, message, send_mail
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm, DoctorRegistrationForm
from django.conf import settings
from django.contrib import messages
from .models import Appointment
from django.views.generic import ListView
import datetime
import random
from django.template import Context
from django.template.loader import render_to_string, get_template


class HomeTemplateView(TemplateView):
    template_name = "index.html"
    
    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        email = EmailMessage(
            subject= f"{name} from doctor family.",
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],
            reply_to=[email]
        )
        email.send()
        return HttpResponse("Email sent successfully!")
    
class StartTemplateView(TemplateView):
    template_name = "home.html"


class AppointmentTemplateView(TemplateView):
    template_name = "appointment.html"

    def post(self, request):
        fname = request.POST.get("fname")
        lname = request.POST.get("fname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        message = request.POST.get("request")

        appointment = Appointment.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            phone=mobile,
            request=message,
        )

        appointment.save()

        messages.add_message(request, messages.SUCCESS, f"Thanks {fname} for making an appointment, we will email you ASAP!")
        return HttpResponseRedirect(request.path)

class ManageAppointmentTemplateView(ListView):
    template_name = "manage-appointments.html"
    model = Appointment
    context_object_name = "appointments"
    login_required = True
    paginate_by = 3


    def post(self, request):
        date = request.POST.get("date")
        appointment_id = request.POST.get("appointment-id")
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.accepted = True
        appointment.accepted_date = datetime.datetime.now()
        appointment.save()

        data = {
            "fname":appointment.first_name,
            "date":date,
        }

        message = get_template('email.html').render(data)
        email = EmailMessage(
            "About your appointment",
            message,
            settings.EMAIL_HOST_USER,
            [appointment.email],
        )
        email.content_subtype = "html"
        email.send()

        messages.add_message(request, messages.SUCCESS, f"You accepted the appointment of {appointment.first_name}")
        return HttpResponseRedirect(request.path)


    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        appointments = Appointment.objects.all()
        context.update({   
            "title":"Manage Appointments"
        })
        return context
    

# Temporary storage for OTPs
otp_storage = {}

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Generate OTP and send email
            otp = random.randint(100000, 999999)
            otp_storage[user.email] = {"otp": otp, "expires_at": now() + timedelta(minutes=10)}
            send_mail(
                "Your OTP Code",
                f"Your OTP code is {otp}. It will expire in 10 minutes.",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            messages.success(request, "OTP sent to your email. Please verify your account.")
            return redirect("otp_verify")
    else:
        form = UserRegistrationForm()
    return render(request, "register.html", {"form": form})


def otp_verify(request):
    if request.method == "POST":
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            otp = form.cleaned_data["otp"]
            if email in otp_storage and otp_storage[email]["otp"] == otp:
                if otp_storage[email]["expires_at"] > now():
                    user = User.objects.get(email=email)
                    user.is_active = True
                    user.save()
                    messages.success(request, "Account verified. You can now log in.")
                    del otp_storage[email]
                    return redirect("login")
                else:
                    messages.error(request, "OTP has expired.")
            else:
                messages.error(request, "Invalid OTP.")
    else:
        form = OTPVerificationForm()
    return render(request, "otp_verify.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("manage")
    else:
        form = UserLoginForm()
    return render(request, "login.html", {"form": form})



def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'your_app_name/profile_list.html', {'profiles': profiles})

def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'your_app_name/appointment_list.html', {'appointments': appointments})

def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorRegistrationForm()
    return render(request, 'register_doctor.html', {'form': form})

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctors})