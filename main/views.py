from django.shortcuts import render, redirect, get_object_or_404
from main.models import Product
from main.forms import ProductForm
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template.loader import render_to_string

# Create your views here.
@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")
    if filter_type == "all":
        products_list = Product.objects.all()
    else:
        products_list = Product.objects.filter(user=request.user)
    context = {
        'nama' : request.user.username,
        'npm' : '2406351440',
        'kelas' : 'PBP C',
        'products_list' : products_list,
        'last_login': request.COOKIES.get('last_login', 'Never'),
    }
    
    return render(request, "main.html", context)

@login_required(login_url='/login')
def get_products_json(request):
    filter_type = request.GET.get("filter", "all")
    if filter_type == "all":
        products_list = Product.objects.all().order_by('-created_at')
    else:
        products_list = Product.objects.filter(user=request.user).order_by('-created_at')
    
    data = []
    for product in products_list:
        data.append({
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'category_display': product.get_category_display(),
            'is_featured': product.is_featured,
            'brand': product.brand,
            'stock': product.stock,
            'sales_count': product.sales_count,
            'created_at': product.created_at.strftime("%b %d, %Y"),
            'user_username' : product.user.username if product.user else None,
            'is_owner' : product.user == request.user if product.user else False,
        })
    return JsonResponse(data, safe=False)

@login_required(login_url='/login')
def create_products(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = ProductForm(request.POST or None)
        if form.is_valid():
            news_entry =  form.save(commit = False)
            news_entry.user = request.user
            news_entry.save()
            return JsonResponse({'status': 'success', 'message': f'Product {news_entry.name}" berhasil dibuat!'}, status=201)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors, 'message': 'Validasi gagal. Mohon periksa kembali input Anda!'}, status=400)
    
    form = ProductForm(request.POST or None)
    if form.is_valid() and request.method == 'POST':
        news_entry = form.save(commit = False)
        news_entry.user = request.user
        news_entry.save()
        messages.success(request, f'Product "{news_entry.name}" berhasil dibuat!')
        return redirect('main:show_main')
    context = {'form': form}
    return render(request, 'create_products.html', context)

@login_required(login_url='/login')
def edit_products(request, id):
    products = get_object_or_404(Product, pk=id)
    if products.user != request.user:
        return JsonResponse({'status': 'error', 'message': 'Anda tidak memiliki izin untuk mengedit produk ini.'}, status=403)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = ProductForm(request.POST or None, instance=products)
        if form.is_valid():
            updated_product = form.save()
            return JsonResponse({'status': 'success', 'message': f'Product "{updated_product.name}" berhasil diperbarui!'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors, 'message': 'Validasi gagal. Mohon periksa kembali input Anda!'}, status=400)
        
    form = ProductForm(request.POST or None, instance=products)
    if form.is_valid() and request.method == 'POST':
        form.save()
        messages.success(request, f'Product "{products.name}" berhasil diperbarui!')
        return redirect('main:show_main')
    context = {'form': form}
    return render(request, "edit_products.html", context)

@login_required(login_url='/login')
def delete_products(request, id):
    products = get_object_or_404(Product, pk=id)
    if products.user != request.user:
        return JsonResponse({'status': 'error', 'message': 'Anda tidak memiliki izin untuk menghapus produk ini.'}, status=403)

    if request.method == 'POST':
        try:
            product_name = products.name
            products.delete()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': f'Product "{product_name}" berhasil dihapus!'}, status=200)
            messages.success(request, f'Product "{product_name}" berhasil dihapus!')
            return HttpResponseRedirect(reverse('main:show_main'))
        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': f'Gagal menghapus produk: {str(e)}'}, status=500)
            messages.error(request, f'Gagal menghapus produk: {str(e)}')
            return HttpResponseRedirect(reverse('main:show_main'))
    return JsonResponse({'status': 'error', 'message': 'Metode tidak diizinkan.'}, status=405)

def register(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Akun Anda berhasil dibuat'}, status=201)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors, 'message': 'Pendaftaran gagal.'}, status=400)
    form = UserCreationForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        form.save()
        messages.success(request, 'Akun Anda berhasil dibuat!')
        return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response_data = {'status': 'success', 'message': f'Selamat datang kembali, {user.username}!', 'redirect_url': reverse("main:show_main")}
            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors, 'message': 'Login gagal. Periksa username dan password Anda.'}, status=400)

    if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        messages.success(request, f'Selamat datang kembali, {user.username}!')
        return response
    
    form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

@login_required(login_url='/login')
def logout_user(request):
    """Menangani LOGOUT, merespons dengan JSON jika AJAX."""
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        logout(request)
        return JsonResponse({'status': 'success', 'message': 'Anda telah keluar.', 'redirect_url': reverse('main:login')}, status=200)

    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    messages.info(request, 'Anda telah keluar.')
    return response

@login_required(login_url='/login')
def get_product_form(request, id=None):
    """Merender konten form (Create/Edit) untuk di-inject ke modal."""
    if id:
        product = get_object_or_404(Product, pk=id, user=request.user)
        form = ProductForm(instance=product)
        form_title = f"Edit Produk: {product.name}"
    else:
        form = ProductForm()
        form_title = "Buat Produk Baru"

    context = {
        'form': form, 
        'form_title': form_title,
        'product_id': id,
    }
    return render(request, 'product_form_content.html', context)

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
