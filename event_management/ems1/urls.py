from django.urls import path
from . import views

#Define list of url patterns

urlpatterns = [
    path('',views.register_view,name='register'),
    path('events/',views.events_view,name='event_list'),
    path('event/<id>',views.event_detailed_view,name="event_detail"),
    path('create/',views.create_event_view,name='create'),
    path('update/<id>/',views.update_event_view,name='update'),
    path('delete/<id>/',views.delete_event_view,name='delete'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('attendee/register/<event_id>/',views.register_attendee,name='attendee_register'),
    path('contact/',views.contact_view,name='contact'),
    path('event/<int:id>/attendees/', views.show_attendees, name='show_attendees'),
]