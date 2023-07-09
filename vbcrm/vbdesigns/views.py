from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from .forms import SignUpForm, AddCustomerForm
from.models import Customer
# Create your views here.


def home(request):
    customers = Customer.objects.all()

    # Check to see if logging in 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authentication
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Login Success")
            return redirect('home')
        else:
            messages.success(request,"Incorrect Username or Password. Try again")
            return redirect ('home')
    else: 
        return render(request, 'home.html', {'customers':customers})

def login_user(request):
    pass

# logout 
def logout_user(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect('home')

# new user registration
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Authenticate the user and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request,"Registeration Success. Welcome")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form':form})
        
    return render(request, 'signup.html', {'form':form})

# customer detail view
def customer_record(request,pk):
    if request.user.is_authenticated:
        customer_record = Customer.objects.get(id=pk)
        return render(request, 'customer.html',{'customer_record':customer_record})
    else:
        messages.success(request,"Please Login to view the details")
        return redirect('home')
    
#  delete a customer 
def delete_customer(request,pk):
     if request.user.is_authenticated:
        customer_delete = Customer.objects.get(id=pk)
        customer_delete.delete()
        messages.success(request,"Successfully deleted the customer")
        return redirect('home')
     else:
        messages.success(request,"Please Login to delete the customer")
        return redirect('home')


# create new customer 
def add_customer(request):
    form = AddCustomerForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_customer = form.save()
                messages.success(request, "Successfully added new customer")
                return redirect('home')
        return render(request,'add_customer.html',{'form':form})
    else:
        messages.success(request, "You must login to add new customer")
        return redirect('home')
    

# update customer
def update_customer(request,pk):
    if request.user.is_authenticated:
        customer_update = Customer.objects.get(id=pk)
        form = AddCustomerForm(request.POST or None, instance=customer_update)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated the customer")
            return redirect('home')
        return render(request,'update_customer.html',{'form':form})
    else:
        messages.success(request, "You must login to update customer")
        return redirect('home')
