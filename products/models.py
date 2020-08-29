from django.db import models

# Create your models here.
class Customer(models.Model):
	name = models.CharField(max_length = 25)

	def __str__(self):
		return self.name

class Products(models.Model):
	title = models.CharField(max_length = 25)
	image = models.FileField()
	description = models.TextField()
	price = models.FloatField()
	created_at = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.title

class Order(models.Model):
	customer = models.CharField(max_length = 25)
	product = models.ForeignKey(Products, on_delete = models.CASCADE)
	quantity = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add = True)

	def __str__(self):
			return self.customer
