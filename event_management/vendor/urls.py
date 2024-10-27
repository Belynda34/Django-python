from django.urls import path
from . import views


urlpatterns=[
    path('vendor/create/',views.create_vendor_view,name='vendor_create'),
    path('allvendors/',views.vendor_view,name='vendor_view'),
    path('vendor/update/<id>',views.update_vendor_view,name='vendor_update'),
    path('vendor/delete/<id>',views.delete_vendor_view,name='vendor_delete'),
]