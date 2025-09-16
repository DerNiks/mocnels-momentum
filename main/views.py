from django.shortcuts import render, redirect, get_object_or_404
from main.models import Product
from main.forms import ProductForm
from django.http import HttpResponse
from django.core import serializers

# Create your views here.
def show_main(request):
    products_list = Product.objects.all()
    context = {
        'nama' : 'Derrick',
        'npm' : '2406351440',
        'kelas' : 'PBP C',
        'products_list' : products_list
    }
    
    return render(request, "main.html", context)

def create_products(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('main:show_main')
    context = {'form': form}
    return render(request, 'create_products.html', context)

def show_products(request, id):
    product = get_object_or_404(Product, pk=id)
    product.increment_sales_count()
    context = {'product' : product}
    return render(request, 'products_details.html', context)
    
def show_xml(request):
    products = Product.objects.all()
    xml_data = serializers.serialize('xml', products)
    return HttpResponse(xml_data, content_type='application/xml')

def show_json(request):
    products = Product.objects.all()
    json_data = serializers.serialize('json', products)
    return HttpResponse(json_data, content_type='application/json')

def show_xml_by_id(request, products_id):
    try:
        products = Product.objects.filter(pk=products_id)
        xml_data = serializers.serialize('xml', products)
        return HttpResponse(xml_data, content_type='application/xml')
    except Product.DoesNotExist:
        return HttpResponse(status=404)

def show_json_by_id(request, products_id):
    try:
        products = Product.objects.filter(pk=products_id)
        json_data = serializers.serialize('json', products)
        return HttpResponse(json_data, content_type='application/json')
    except Product.DoesNotExist:
        return HttpResponse(status=404)

