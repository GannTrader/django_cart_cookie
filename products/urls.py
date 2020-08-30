from django.urls import path
from .import views
app_name = 'products'

urlpatterns = [
	path('', views.product, name = 'product'),
	path('addtocart/<int:pk>', views.addtocart, name = 'addtocart'),
	path('viewCart/', views.viewCart, name = 'viewCart'),
	path('deleteCart/<int:id>', views.deleteCart, name = 'deleteCart'),
]