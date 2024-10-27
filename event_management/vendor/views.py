from django.shortcuts import render
from django.contrib import messages
from .form import VendorForm
from django.shortcuts import redirect
from .models import Vendor
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.


@login_required
def vendor_view(request):
    vendors = Vendor.objects.all()
    return render(request,'vendors/vendor_view.html',{'vendors':vendors})


def create_vendor_view(request):
    if request.method == "POST":
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vendor_view')
    else:
        form=VendorForm()
        return render(request,'vendors/create_vendor.html',{'form':form})

# def vendor_view(request):
#     vendor_list = Vendor.objects.all()
#     paginator = Paginator(vendor_list,10)
#     page_number=request.GET.get('page')
    
#     vendors_pages = paginator.get_page(page_number)

#     return render(request,'vendors/vendor_view.html',{'vendors':vendors_pages})
    


def update_vendor_view(request,id):
    vendor = Vendor.objects.get(id=id)
    if request.method == "POST":
        form =VendorForm(request.POST,instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('vendor_view')
    else:
        form = VendorForm(instance=vendor)
        return render(request,'vendors/update_vendor.html',{'form':form})
    


def delete_vendor_view(request,id):
    vendor=Vendor.objects.get(id=id)
    if request.method == "POST":
        vendor.delete()
        messages.success(request,'Event deleted successfully')
        return redirect('vendor_view')
    return render(request,'vendors/delete_vendor.html',{'vendor':vendor})