from django.shortcuts import render, redirect
from .models import*
from .forms import orderForm, CreateUserForm,customerForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . decorators import unauthenticated_user, allowed_users, admin_only
n 

# Create your views here.
@login_required(login_url='loginPage')
@admin_only
def home(request):
	customers=Customer.objects.all()
	orders=Order.objects.all()
	total_customers = customers.count()
	total_orders = orders.count()
	Delivered = orders.filter(status='Delivered').count()
	Pending = orders.filter(status='Pending').count()
	context = {'customers':customers, 'orders':orders,'total_orders':total_orders,'Delivered':Delivered,'Pending':Pending}
	return render(request, "accounts/dashboard.html",context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()	
	return render(request,"accounts/products.html", {'products': products})

@login_required(login_url='loginPage')
def customer(request,pk_test):	
	customer=Customer.objects.get(id=pk_test)
	orders=customer.order_set.all()
	order_count = orders.count()
	myFilter=OrderFilter(request.GET, queryset=orders)
	orders=myFilter.qs
	context= {'customer':customer, 'orders':orders,'order_count':order_count, 'myFilter':myFilter}
	return render(request, "accounts/customer.html",context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def create_Order(request,pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=6)
	customer=Customer.objects.get(id=pk)
	formset=OrderFormSet(queryset=Order.objects.none(), instance=customer)
	#form=orderForm(initial={'customer':customer})
	if request.method=="POST":
		#form=orderForm(request.POST)
		formset=OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')
	context={'formset':formset, 'customer':customer}
	return render(request, "accounts/order_form.html", context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def update_Order(request,pk):
	order=Order.objects.get(id=pk)
	form=orderForm(instance=order)
	if request.method=="POST":
		form=orderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')
	context={'order':order,'form':form}
	return render(request, "accounts/order_form.html", context)	

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def delete_Order(request, pk):
	order=Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')
	context={'order':order}
	return render(request, "accounts/delete_form.html", context)

@unauthenticated_user
def loginPage(request):
	
	if request.method=="POST":
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(request, username=username, password=password)

		if user is not None:
			login(request,user)
			return redirect('home')
		else:
			messages.info(request, 'Username Or Password wrong')

	context={}
	return render(request, "accounts/login.html", context)


@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method=="POST":
		form=CreateUserForm(request.POST)

		if form.is_valid():
			user=form.save()
			username = form.cleaned_data.get('username')
			
			messages.success(request, 'Account was created' +username)

			return redirect('loginPage')


	context={'form': form}
	return render(request, "accounts/register.html", context)


def logoutPage(request):
	logout(request)

	return redirect('loginPage')

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all()

	total_orders = orders.count()
	Delivered = orders.filter(status='Delivered').count()
	Pending = orders.filter(status='Pending').count()

	context={'orders':orders, 'total_orders':total_orders, 'Delivered':Delivered, 'Pending':Pending}
	return render (request, "accounts/user.html", context)	

def settingPage(request):

	customer = request.user.customer
	form = customerForm(instance=customer)

	if request.method == 'POST':
		form = customerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()

	
	context={'form':form}

	return render(request, "accounts/setting.html", context)
