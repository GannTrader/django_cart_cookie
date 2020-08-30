from django.shortcuts import render, redirect
from .models import Products, Order
from django.utils.crypto import get_random_string
from django.http import HttpResponse
# Create your views here.
def product(request):
	listproduct = Products.objects.all()
	return render(request, 'products/listproduct.html', {'product': listproduct})

def addtocart(request, pk):
	# nếu user login, ta add vào bảng order bình thường
	# nếu chưa login ta sẽ tạo cookie (nếu chưa có cookie) và add vô bảng như user login
	# quan trong là khi bảng order sẽ có quá nhiều dữ liệu dạng guest giỏ hàng thì phải xóa đi sau 1 thời gian nhất định với ebay =90 days => tạo 1 code chạy để xác định xem cái nào = 90 thông qua created_at trong bảng Order
	product = Products.objects.get(pk = pk)
	
	if str(request.user) != 'AnonymousUser':
		customer = Order.objects.filter(customer = request.user)

		if customer.exists():
			if Order.objects.filter(customer = request.user, product = product).exists():
				customerExit = Order.objects.get(customer = request.user, product = product)
				customerExit.quantity += 1
				customerExit.save()
			else:
				Order.objects.create(
					customer = request.user,
					product = product,
					quantity = 1
				)
		else:
			Order.objects.create(
				customer = request.user,
				product = product,
				quantity = 1
			)
	else:
		if not request.COOKIES.get('customer'):
			customer = get_random_string(length = 25)
			response = render(request, 'products/listproduct.html')
			response.set_cookie('customer', customer, 60*60*24*30)

			Order.objects.create(
				customer = customer,
				product = product,
				quantity = 1
			)	
			return response
		else:
			customerExit = Order.objects.filter(customer = str(request.COOKIES['customer']), product = product)
			if customerExit.exists():
				customerExit = Order.objects.get(customer = str(request.COOKIES['customer']), product = product)
				customerExit.quantity += 1
				customerExit.save()
			else:
				Order.objects.create(
					customer = str(request.COOKIES['customer']),
					product = product,
					quantity = 1
				)
	return redirect('products:product')