from email.message import EmailMessage
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from Stocker import settings
from products.models import Category, Product, Supplier
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages

# Create your views here.


def home_view(request:HttpRequest):

    products = Product.objects.all()
    products_count = Product.objects.all()
    products_low_stock = Product.objects.filter(quantity__lte=5)

    search_query = request.GET.get("search")
    if search_query and len(search_query) >= 1:
        products = products.filter(name__icontains=search_query)

    category_id = request.GET.get("category")
    if category_id:
        products = products.filter(category__id=category_id)

    supplier_id = request.GET.get("supplier")
    if supplier_id:
        products = products.filter(suppliers__id=supplier_id)
        
            
        
    order_by = request.GET.get("order_by")
    if order_by == "price":
        products = products.order_by("-price")
    elif order_by == "created_at":
        products = products.order_by("-created_at")
    
        
        
    page_number = request.GET.get("page", 1)
    paginator = Paginator(products, 9)
    products_page = paginator.get_page(page_number)


    context = {
        "categories": Category.objects.all(),
        "suppliers": Supplier.objects.all(),
        "products" : products_page,
        "products_count" : products_count,
        "products_low_stock": products_low_stock,        
    }
    return render(request, "main/index.html", context)

def mode_view(request:HttpRequest, mode):

    response = redirect(request.GET.get("next", "/"))

    if mode == "light":
        response.set_cookie("mode", "light")
    elif mode == "dark":
        response.set_cookie("mode", "dark")


    return response


