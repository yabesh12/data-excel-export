from django.urls import path
from .import views

urlpatterns = [
	path('home/', views.home, name="home"),
	path('sales-list/<int:pk>', views.sales_list, name="sales_list"),
	path('download-data/<int:pk>', views.download_list, name="download_list"),
]