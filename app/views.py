from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.template import loader
import datetime
from django.shortcuts import render, get_object_or_404, render_to_response
from django.urls import reverse
from django.views.generic.edit import CreateView
from .forms import RegisterForm, UserAuthenticationForm
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.timezone import now
from django.utils import timezone
from django.views import generic
from django.db.models import Avg, Count, Min, Sum
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Account,DoctorDepartment,Appointment,RateModel
from datetime import date
  
def contactpage(request): 
    context = {}
    return render(request, "app/contactpage.html", context)


def whoarewe(request):
    context = {}
    return render(request, "app/whoarewe.html", context)


def homepage(request):
    context = {}
    return render(request, "app/homepage.html", context)

    
def register_view(request):
    context = {}
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
         
            form.save()
            
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            
            login(request, user)
            return redirect('home')
        else:
            context['reg_form'] = form
    else:
        form = RegisterForm()
        context['reg_form'] = form
    return render(request, 'app/register.html', context)



@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    if request.POST:
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request,user)
                return redirect('home')
    else:
        form = UserAuthenticationForm()
    context['login_form'] = form
    return render(request,'app/login.html',context)

@login_required
def dept_select(request):
    context = {}

    #Productorder.objects.all().distinct('category')
    datas = DoctorDepartment.objects.all()
    context['data'] = datas
    return render(request, 'app/dept_select.html', context)

@login_required
def doctor_select(request, pk):
    context = {}
    doctors = DoctorDepartment.objects.filter(department = pk)
    context['doctor'] = doctors
    return render(request, 'app/doctorlist.html', context)

@login_required
def schedule_view(request, pk):
    context = {}
    kisi = get_object_or_404(Account, username = pk)
    data = DoctorDepartment.objects.get(user = kisi)

    app_times = Appointment.objects.filter(appointment_with = data, user__isnull = True, old = False)

    context['app_time'] = app_times
    return render(request, 'app/schedule.html', context)

@login_required
def appointment(request, pk):
    context = {}
    user = request.user
    app_data = Appointment.objects.get(id = pk)
    new_data = Appointment.objects.filter(user=user, date=app_data.date, time_start = app_data.time_start, time_end = app_data.time_end)
    if new_data:
        err_msg = "Lütfen randevularınızı kontrol edin"
        return render(request, 'app/myappointments.html', {'err_msg':err_msg})
    else :
        app_data.user = user
        app_data.save()
        all_app = Appointment.objects.filter(user = user).order_by('date', 'time_start')
        context['data'] = all_app
        return render(request, 'app/myappointments.html', context)


@login_required
def rate_app(request, pk):
    context = {}
    user = request.user
    # pk = item.id
    app_data = Appointment.objects.get(id = pk)
    if 'rate1' in request.POST :
        app_data.app_rate = 1
        app_data.save()
    if 'rate2' in request.POST :
        app_data.app_rate = 2
        app_data.save()
    if 'rate3' in request.POST :
        app_data.app_rate = 3
        app_data.save()
    app_data.save()
    all_app = Appointment.objects.filter(user = user).order_by('date', 'time_start')
    context['data'] = all_app
    return render(request, 'app/myappointments.html', context)

    



@login_required
def appointmentdata(request):
    context = {}
    user = request.user
    all_app = Appointment.objects.filter(user = user)
    today = datetime.date.today()
    Appointment.objects.filter(date__lte = today).update(old=True)
    all_apps = Appointment.objects.filter(user=user).order_by('date', 'time_start')
    context['data'] = all_apps
    return render(request, 'app/myappointments.html', context)

@login_required
def delete_appointment(request, pk):
    context = {}
    user = request.user
    Appointment.objects.filter(id = pk).update(user = None)
    all_app = Appointment.objects.filter(user = user)
    context['data'] = all_app
    return render(request, 'app/myappointments.html', context)

@login_required
def blog(request):
    context = {}
    user = request.user
    all_app = Appointment.objects.filter(user = user)
    context['data'] = all_app
    return render(request, 'app/blog.html', context)

def time_check(data):
    for pk in data:
        data1 = Appointment.objects.get(id=pk.id)
        today = datetime.date.today()
        hour = datetime.datetime.now().time()
        if data1.date < today:
            data1.old = True
            data1.save()
        if data1.date == today:
            if data1.time_start < hour:
                data1.old = True
            data1.save()
        else:
            data1.old = False
            data1.save()


@login_required
def appointmentdoc(request):
    context = {}
    user_data = request.user
    doctor = DoctorDepartment.objects.get(user = user_data)
    all_app = Appointment.objects.filter(appointment_with = doctor)
    context['data'] = all_app
    return render(request, 'app/doctorappointment.html', context)

