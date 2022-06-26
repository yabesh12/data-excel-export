from django.db import models
from django.urls import reverse

# Create your models here.
POSITION = (
	("Employee", "Employee"),
	("Executive", "Executive"),
	("Manager", "Manager"),
	)

class SalesExecutive(models.Model):
	name = models.CharField(max_length=200)
	position = models.CharField(max_length=200, choices=POSITION, default="Employee")

	def __str__(self):
		return f"{self.id} - {self.name} - {self.position}"

	def get_absolute_url(self):
		return reverse('sales_list', args=[self.id])


class Lead(models.Model):
	sales_executive = models.ForeignKey("SalesExecutive", on_delete=models.CASCADE, related_name="lead_sales")
	invoice_no = models.CharField(max_length=100)
	invoice_amount = models.PositiveIntegerField()

	def __str__(self):
		return f"{self.id} - {self.sales_executive} - {self.invoice_no}"