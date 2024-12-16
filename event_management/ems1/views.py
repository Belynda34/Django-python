import os
from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
# from django.views import View
from .models import Event,UserAccount,Attendee,Analytics
from .form import EventForm,RegisterForm,LoginForm,AttendeeForm
import json
from django.core.paginator import Paginator

from django.views.decorators.csrf import csrf_exempt
# from rest_framework import serializers

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
            Analytics.objects.create(action="user_registered",user=user)
            registrations = Analytics.objects.filter(action="user_registered").count()
            messages.success(request, f"Welcome {username}! Total registrations: {registrations}")
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
    




def event_view_po(request):
    # user_role = None
    events = Event.objects.all()  # Default to an empty queryset

    # if request.user.is_authenticated:
    #     user_role = request.user.useraccount.user_role
    #     if user_role == "event manager":
    #         events = Event.objects.filter(created_by=request.user)
    #     elif user_role == "attendee":
    #         events = Event.objects.all()

    registrations = Analytics.objects.filter(action="user_registered").count()

    # Prepare data for all events
    events_data = [
        {
            'id': event.id,
            'name': event.name,
            'description': event.description,
            'location': event.location,
            'created_by': event.created_by,  # Assuming 'created_by' is a User object
        }
        for event in events
    ]

    return JsonResponse({
        'events': events_data,
        # 'user_role': user_role,
        'registrations': registrations
    })


def events_view(request):
    events = Event.objects.all().order_by('id')
    paginator = Paginator(events, 10)  # Adjust page size as needed

    try:
        page_number = int(request.GET.get('page', 1))
    except ValueError:
        page_number = 1

    event_page = paginator.get_page(page_number)
    registrations = Analytics.objects.filter(action="user_registered").count()

    return render(request, 'events/event_view.html', {'page_obj': event_page, 'registrations': registrations})









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
# def show_attendees(request,id):
#     event = Event.objects.get(id=id)
#     attendees = Attendee.objects.filter(event=event)

#     return render(request, 'events/show_attendees.html', {
#         'event': event,
#         'attendees': attendees
#     })




# def show_attendees(request, event_id):
#     # Use get_object_or_404 to safely handle invalid IDs
#     event = Event.objects.get(id=event_id)
    
#     # Filter attendees by the event
#     attendees = Attendee.objects.filter(event=event)

#     # Prepare the list of attendees to return as JSON
#     attendees_data = [
#         {
#             'event_id': attendee.event,
#             'name': attendee.name,
#             'email': attendee.email,
#             # Add more fields as necessary
#         }
#         for attendee in attendees
#     ]

#     # Return the response as a JSON object
#     return JsonResponse({
#         # 'event': {
#         #     'event_id': event.id,
#         # },
#         'attendees': attendees_data
#     })


# def show_attendees(request, event_id):
#     # Assuming you have an event with the given ID
#     event = Event.objects.get(id=event_id)
    
#     # Serialize the Event object into a JSON-compatible format
#     event_data = serializers.serialize('json', [event])

#     # You may want to serialize attendees as well
#     attendees = Attendee.objects.filter(event=event)
#     attendees_data = list(attendees.values())  # This will return a list of dictionaries

#     return JsonResponse({
#         'event': event_data,
#         'attendees': attendees_data
#     })

def all_attendees(request):
    # Fetch all attendees
    attendees = Attendee.objects.all()

    # Convert the queryset to a list of dictionaries
    attendees_data = list(attendees.values())  # .values() converts the queryset to dictionaries

    # Return the data as a JSON response
    return JsonResponse({
        'attendees': attendees_data
    })



# SHOWING DETAILS FOR AN EVENT 
def event_detailed_view(request,id):
    # user_role:None
    # if request.user.is_authenticated:
      # user_role=request.user.useraccount.user_role
    event = Event.objects.get(id=id)
    event_data = [
        {
            'id':event.id,
            'name':event.name,
            'description':event.description,
            'location':event.location
        }
    ]
    # return render(request,'events/event_detailed.html',{'event':event})
    return JsonResponse({
        'event':event_data
    })


# CONTACT VIEW
def contact_view(request):
    return render(request,'events/contact.html')


# def show_attendees(request, event_id):
#     # Retrieve the Event object by event_id
#     try:
#         event = Event.objects.get(id=event_id)
#     except Event.DoesNotExist:
#         return JsonResponse({'error': 'Event not found'}, status=404)

#     # Use the correct field name, event_id
#     attendees = Attendee.objects.filter(event_id=event.id)
    
#     # Serialize event and attendees
#     event_serializer = Eventserializer(event)
#     attendees_serializer = AttendeeSerializer(attendees, many=True) # type: ignore
    
#     # Return a JSON response
#     return JsonResponse({
#         'event': event_serializer.data,
#         'attendees': attendees_serializer.data
#     })

  
# CREATE EVENT
 
# @login_required
def create_event_view(request):
    user_role = None
    if request.user.is_authenticated:
        user_role = request.user.useraccount.user_role
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            # form.save()
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            Analytics.objects.create(action="event_created",user=request.user,event=event)
            messages.success(request, "Event created successfully!")
            return redirect('event_list')
        else:
            messages.error(request,"Please correct the errors below")
    else:
        form=EventForm()
    return render(request,'events/create_event.html',{'form':form,'user_role':user_role})



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





# Analytics view 

@login_required
def analytics_view(request):
    event_counts = Event.objects.annotate(attendee_count=Count('attendees')).values('name', 'attendee_count')
    user_registrations = Analytics.objects.filter(action="user_registered").count()
    event_creations = Analytics.objects.filter(action="event_created").count()

    serialized_event_counts = json.dumps(list(event_counts))

    print(event_counts, user_registrations, event_creations)
    return render(request, 'events/analytics.html', {
        'event_counts': serialized_event_counts,
        'user_registrations': user_registrations,
        'event_creations': event_creations
    })







