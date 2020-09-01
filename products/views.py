from django.shortcuts import render, redirect
from .models import Products, Order
from django.utils.crypto import get_random_string
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate

# Create your views here.
def product(request):
	listproduct = Products.objects.filter(status = 'active')
	return render(request, 'products/listproduct.html', {'product': listproduct})

def addtocart(request, pk):
	# nếu user login, ta add vào bảng order bình thường
	# nếu chưa login ta sẽ tạo cookie (nếu chưa có cookie) và add vô bảng như user login
	# quan trong là khi bảng order sẽ có quá nhiều dữ liệu dạng guest giỏ hàng thì phải xóa đi sau 1 thời gian nhất định với ebay =90 days => tạo 1 code chạy để xác định xem cái nào = 90 thông qua created_at trong bảng Order
	product = Products.objects.get(pk = pk)
	
	if request.user.is_authenticated:
		customer = Order.objects.filter(customer = request.user)

		if customer.exists():
			if Order.objects.filter(customer = request.user, product = product).exists():
				customerExit = Order.objects.get(customer = request.user, product = product)
				customerExit.quantity += 1
				customerExit.save()
				messages.success(request, 'your add more than 1 item in your cart')

			else:
				Order.objects.create(
					customer = request.user,
					product = product,
					quantity = 1,
					price = product.price
				)
				messages.info(request, 'your add 1 item in your cart')

		else:
			Order.objects.create(
				customer = request.user,
				product = product,
				quantity = 1,
				price = product.price
			)
			messages.info(request, 'your add 1 item in your cart')

	else:
		if not request.COOKIES.get('customer'):
			customer = get_random_string(length = 25)
			response.set_cookie('customer', customer, 60*60*24*30)

			Order.objects.create(
				customer = customer,
				product = product,
				quantity = 1,
				price = product.price
			)	
			messages.info(request, 'your add 1 item in your cart')
		else:
			customerExit = Order.objects.filter(customer = str(request.COOKIES['customer']), product = product)
			if customerExit.exists():
				customerExit = Order.objects.get(customer = str(request.COOKIES['customer']), product = product)
				customerExit.quantity += 1
				customerExit.save()
				messages.warning(request, 'your add more than 1 item in your cart')

			else:
				Order.objects.create(
					customer = str(request.COOKIES['customer']),
					product = product,
					quantity = 1,
					price = product.price
				)
				messages.info(request, 'your add 1 item in your cart')

	return redirect('products:product')

def viewCart(request):
	total = 0
	if request.user.is_authenticated:
		yourCart = Order.objects.filter(customer = request.user)
		if yourCart.exists():
			for item in yourCart:
				total += item.price * item.quantity
			return render(request, 'products/viewCart.html', {'yourCart': yourCart, 'total': total})
		else:
			messages.info(request, 'your cart do not have any product')
			return render(request, 'products/viewCart.html', {'total': total})
	else:
		yourCart = Order.objects.filter(customer = str(request.COOKIES['customer']))
		if yourCart.exists():
			for item in yourCart:
				total += item.price * item.quantity
			return render(request, 'products/viewCart.html', {'yourCart': yourCart, 'total': total})
		else:
			messages.info(request, 'your cart do not have any product')
			return render(request, 'products/viewCart.html', {'total': total})

def deleteCart(request, id):
	product = Products.objects.get(id=id)
	Order.objects.filter(product = product).delete()
	return redirect('products:viewCart')

def updateCart(request):
	id = request.POST.get('id')
	number = request.POST.get('number')

	product = Products.objects.get(id = id)
	Order.objects.filter(product=product).update(quantity = number)
	return redirect('products:viewCart')