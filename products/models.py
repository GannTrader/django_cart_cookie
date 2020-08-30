from django.db import models

# Create your models here.
STATUS = (
	('active', 'active'),
	('inactive', 'inactive')
	)
class Products(models.Model):
	title = models.CharField(max_length = 25)
	image = models.FileField()
	description = models.TextField()
	price = models.FloatField()
	created_at = models.DateTimeField(auto_now_add = True)
	status = models.CharField(max_length = 25, choices = STATUS)

	def __str__(self):
		return f"{self.title} -- {self.status}"

class Order(models.Model):
	customer = models.CharField(max_length = 25)
	product = models.ForeignKey(Products, on_delete = models.CASCADE)
	quantity = models.IntegerField()
	price = models.FloatField()
	created_at = models.DateTimeField(auto_now_add = True)

	def __str__(self):
			return f"{self.customer} -- {self.product} --- {self.quantity}"
