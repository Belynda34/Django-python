from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
# from django.views import View
from .models import Event,UserAccount,Attendee
from .form import EventForm,RegisterForm,LoginForm,AttendeeForm

# Create your views here.


# Registering the user
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user_role = form.cleaned_data.get("user_role")

            user=User.objects.create_user(username=username,email=email,password=password)
            UserAccount.objects.create(user=user,user_role=user_role)
            login(request,user)
            return redirect('event_list')
    else:
        form=RegisterForm()
    return render(request,'events/register.html',{'form':form})

# Login for the user
def login_view(request):
    error_message=None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('event_list')
            else:
                error_message="Invalid credentials"
    else:
        form=LoginForm()
    return render(request,'events/login.html',{'form':form,'error':error_message})           

# logging out the user
def logout_view(request):
    logout(request)
    return redirect('login')
    
# Displaying all available events
@login_required
def events_view(request):
    user_role = None
    if request.user.is_authenticated:
        user_role=request.user.useraccount.user_role
    events = Event.objects.all()
    return render(request,'events/event_view.html',{'events':events,'user_role':user_role})

def create_event_view(request):
    if request.user.is_authenticated:
            user_role=request.user.useraccount.user_role
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form=EventForm()
    return render(request,'events/create_event.html',{'form':form,'user_role':user_role})

# REGISTER ATTENDEE FOR AN EVENT 
def register_attendee(request,event_id):
    event=Event.objects.get(id=event_id)
    if request.method == "POST":
        form = AttendeeForm(request.POST)
        if form.is_valid():
            attendee=form.save(commit=False)
            attendee.event=event
            attendee.save()
            return render(request,'events/success.html',{'event_name':event.name})
    else:
        form=AttendeeForm()
    return render(request,'events/attendee_register.html',{'form':form,'event':event})

# SHOW ATTENDEES FOR AN EVENT 
def show_attendees(request,id):
    event = Event.objects.get(id=id)
    attendees = Attendee.objects.filter(event=event)

    return render(request, 'events/show_attendees.html', {
        'event': event,
        'attendees': attendees
    })

  
# CREATE EVENT 


# UPDATING AN EVENT 
def  update_event_view(request,id):
    event = Event.objects.get(id=id)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request,'events/update_view.html',{'form':form})

#DELETING AN EVENT  
def delete_event_view(request,id):
    event = Event.objects.get(id=id)
    if request.method == "POST":
        event.delete()
        messages.success(request,'Event deleted successfully')
        return redirect('event_list')
    return render(request,"events/delete_event.html",{'event':event})


# SHOWING DETAILS FOR AN EVENT 
def event_detailed_view(request,id):
    user_role:None
    if request.user.is_authenticated:
        user_role=request.user.useraccount.user_role
    event = Event.objects.get(id=id)
    return render(request,'events/event_detailed.html',{'event':event,'user_role':user_role})


# CONTACT VIEW
def contact_view(request):
    return render(request,'events/contact.html')







