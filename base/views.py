from django.shortcuts import render
from django.http import HttpResponse
from .models import Lead, SalesExecutive
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
import xlwt
import datetime


def home(request):
	data = SalesExecutive.objects.all()
	print(data)
	qs_json = serializers.serialize('json', data)
	return render(request, 'index.html', {'data':data})


def get_data(pk):
	sales_instance = get_object_or_404(SalesExecutive, id=pk)

	leads = sales_instance.lead_sales.all()	

	context = {'leads':leads,'sales_instance':sales_instance}
	return context

def sales_list(request, pk):
	context = get_data(pk)

	return render(request, 'sales_list.html', context)

	
def download_list(request, pk):
	data = get_data(pk)
	print(data)
	# content-type of response
	response = HttpResponse(content_type='application/ms-excel')

	#decide file name
	response['Content-Disposition'] = 'attachment; filename=Sales' + \
	    str(datetime.datetime.now()) + '.xls'

	#creating workbook
	wb = xlwt.Workbook(encoding='utf-8')

	#adding sheet
	ws = wb.add_sheet("Products")

	# Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	date_style = xlwt.XFStyle()
	date_style.num_format_str = 'DD-MM-YY'

	# headers are bold
	font_style.font.bold = True

	#column header names, you can use your own headers here
	columns = ['Name', 'Position', 'Invoice Number', 'Invoice Amount']

	#write column headers in sheet
	for col_num in range(len(columns)):
	    ws.write(row_num, col_num, columns[col_num], font_style)

	# Sheet body, remaining rows
	font_style = xlwt.XFStyle()
	# rows = ProductVariants.objects.all().values_list('created','edited','vendoruser','product_id',
	#                                             'item_num','variant_value','initial_stock','approval_status',
	#                                             'approved_date','approved_by',)


	rows = [value for value in data.get('leads')]
	print(rows)
	# for row in rows:
	# 	row_num +=  1
	# 	# print(row_num)
	for row in rows:
		for col_num in range(len(rows)):
		    ws.write(row_num, col_num,str(row[col_num]), font_style)           

	wb.save(response)
	return response