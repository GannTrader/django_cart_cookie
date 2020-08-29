from django.urls import path
from .import views
app_name = 'products'

urlpatterns = [
	path('', views.product),
	path('addtocart/<int:pk>', views.addtocart, name = 'addtocart'),
]