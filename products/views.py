from django.shortcuts import render
from .models import Products, Order

# Create your views here.
def product(request):
	listproduct = Products.objects.all()
	return render(request, 'products/listproduct.html', {'product': listproduct})

def addtocart(request, pk):
	# nếu user login, ta add vào bảng order bình thường
	# nếu chưa login ta sẽ tạo cookie (nếu chưa có cookie) và add vô bảng như user login
	if request.user is not None:
		customer = Order.objects.filter(customer = request.user)

		if customer.exists():
			customerExit = Order.objects.get(customer = request.user)
			customerExit.quantity = int(customerExit.quantity) + 1
			print(customerExit.quantity)
		else:
			Order.objects.create(
				customer = request.user,
				product = Products.objects.get(pk = pk),
				quantity = 1
			)