import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Sum, F, Q
from Stocker import settings
from .models import Product, Category, Supplier
from django.http import HttpRequest, HttpResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from datetime import datetime, timezone
from django.templatetags.static import static


def update_product_view(request, product_id):
    product = Product.objects.get( pk=product_id)

    categories = Category.objects.all()
    suppliers = Supplier.objects.all()

    if request.method == 'POST':
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.quantity = int(request.POST['quantity']) 
        product.category = Category.objects.get(id=request.POST['category'])

        if 'image' in request.FILES:
            product.image = request.FILES['image']

        product.save()

        selected_suppliers = Supplier.objects.filter(
            id__in=request.POST.getlist('suppliers')
        )
        product.suppliers.set(selected_suppliers)

        if product.quantity < 5:
            content_html = render_to_string(
                "main/mail/low_stock.html",
                {"product": product , "quantity": product.quantity,}  
            )
            send_to = ["hassan8abdulla@gmail.com"]  
            email_message = EmailMessage(
                f"Low Stock Alert: {product.name} — {product.quantity} left",
                content_html,
                settings.EMAIL_HOST_USER,
                send_to
            )
            email_message.content_subtype = "html"
            email_message.send()

        messages.success(request, "Product updated successfully!")
        return redirect('products:admin_product_view')

    return render(request, 'products/update_product.html', {
        'product': product,
        'categories': categories,
        'suppliers': suppliers,
    })

def add_supplier_view(request: HttpRequest):
    if request.method == "POST":
        name = request.POST["name"]
        contact_email = request.POST["contact_email"]
        contact_phone = request.POST["contact_phone"]
        logo = request.FILES.get("logo")

        if Supplier.objects.filter(name=name).exists():
            messages.error(request, "A supplier with this name already exists.")
            return redirect('products:admin_supplier_view')

        new_supplier = Supplier(
            name=name,
            contact_email=contact_email,
            contact_phone=contact_phone,
            logo=logo,
        )
        new_supplier.save()

        messages.success(request, "Supplier added successfully!")
        return redirect('products:admin_supplier_view')

    return render(request, "products/add_supplier.html")

def supplier_detail_view(request, supplier_id):
    supplier = Supplier.objects.get(pk=supplier_id)
    related_suppliers = Supplier.objects.exclude(id=supplier.id).all()  
    
    return render(request, 'products/supplier_detail.html', {
        'supplier': supplier,
        'related_suppliers': related_suppliers,
    })

    
def admin_supplier_view(request):
    suppliers = Supplier.objects.all()
    return render(request, 'products/admin_supplier.html', {'suppliers': suppliers})

def update_supplier_view(request, supplier_id):
    supplier = Supplier.objects.get(pk=supplier_id)

    if request.method == 'POST':
        supplier.name = request.POST['name']
        supplier.contact_email = request.POST['contact_email']
        supplier.contact_phone = request.POST['contact_phone']

        if request.FILES.get('logo'):
            supplier.logo = request.FILES['logo']

        supplier.save()
        messages.success(request, "Supplier updated successfully!")
        return redirect('products:admin_supplier_view')  

    return render(request, 'products/update_supplier.html', {'supplier': supplier})

def delete_supplier_view(request: HttpRequest, supplier_id: int):
    supplier = Supplier.objects.get(pk=supplier_id)
    supplier.delete()
    messages.success(request, f"Supplier '{supplier.name}' was deleted successfully.")
    return redirect('products:admin_supplier_view')

def display_all_suppliers_view(request: HttpRequest):
    suppliers = Supplier.objects.all()
  
    return render(request, "products/all_suppliers.html", {"suppliers" : suppliers})

def add_category_view(request: HttpRequest):
    if request.method == "POST":
        category_name = request.POST["name"]
        
        if Category.objects.filter(name=category_name).exists():
            messages.error(request, "A category with this name already exists.")
            return render(request, "products/add_category.html")
        
      
        new_category = Category(
            name=category_name,
            description=request.POST.get("description", ""),
        )
        new_category.save()

        messages.success(request, f"Monitor '{new_category.name}' added successfully.")
        return redirect('products:admin_category_view')  

    return render(request, "products/add_category.html") 

def update_category_view(request, category_id):
    category = Category.objects.get(pk=category_id)

    if request.method == 'POST':
        category.name = request.POST['name']
        category.description = request.POST['description']

        category.save()
        messages.success(request, "Category updated successfully!")
        return redirect('products:admin_category_view')  

    return render(request, 'products/update_category.html', {'category': category})

def admin_category_view(request):
    categories = Category.objects.all()
    return render(request, 'products/admin_category.html', {'categories': categories})

def category_detail_view(request, category_id):
    category = Category.objects.get(pk=category_id)
    related_categories = Category.objects.exclude(id=category.id).all()  
    
    return render(request, 'products/category_detail.html', {
        'category': category,
        'related_categories': related_categories,
    })
    
def delete_product_view(request, product_id):
    product =Product.objects.get(pk=product_id)
    product.delete()
    messages.success(request, f"Product '{product.name}' was deleted successfully.")
    return redirect('products:admin_product_view')

def delete_category_view(request: HttpRequest, category_id: int):
    category = Category.objects.get(pk=category_id)
    category.delete()
    messages.success(request, f"Category '{category.name}' was deleted successfully.")
    return redirect('products:admin_category_view') 

def display_all_categories_view(request: HttpRequest):
    categories = Category.objects.all()
  
    return render(request, "products/all_categories.html", {"categories" : categories})


def add_product_view(request: HttpRequest):
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()  

    if request.method == "POST":
       category_name = request.POST["category"]
       category = Category.objects.get(name=category_name)   
       
       selected_suppliers = Supplier.objects.filter(id__in=request.POST.getlist("suppliers"))
       new_product = Product(
            name=request.POST["name"],
            description=request.POST["description"],
            price=request.POST["price"],
            quantity=request.POST["quantity"],
            category=category,
            image=request.FILES["image"],
        )
       new_product.save()
       new_product.suppliers.set(selected_suppliers)

       messages.success(request, "Product added successfully!")
       return redirect('main:home_view')

    return render(request, "products/add_product.html" , {'categories' : categories ,'suppliers': suppliers,})

def product_detail_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id).all()
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })


def display_all_products_view(request: HttpRequest):
    products = Product.objects.all()  
  
    return render(request, "products/all_products.html", {"products": products})



def admin_product_view(request):
    products = Product.objects.all()  
    return render(request, 'products/admin_product.html', {'products': products})


def search_products_view(request: HttpRequest):
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

    context = {
        "products": products.distinct(),
        "categories": Category.objects.all(),
        "suppliers": Supplier.objects.all(),
        "products_count" : products_count,
        "products_low_stock" : products_low_stock,
    }
    return render(request, "main/index.html", context)

def inventory_report_view(request):
    products = (
        Product.objects
        .select_related('category')
        .prefetch_related('suppliers')
        .annotate(stock_value=F('price') * F('quantity'))
    )

    total_products = products.count()
    total_quantity = products.aggregate(total_qty=Sum('quantity'))['total_qty'] or 0
    total_stock_value = products.aggregate(total_val=Sum(F('price') * F('quantity')))['total_val'] or 0

    LOW_STOCK_THRESHOLD = 5
    low_stock = products.filter(quantity__lt=LOW_STOCK_THRESHOLD)
    low_stock_count = low_stock.count()

    summary_by_category = (
        Category.objects
        .annotate(
            num_products=Count('products', distinct=True),
            quantity=Sum('products__quantity'),
            stock_value=Sum(F('products__price') * F('products__quantity'))
        )
        .values(
            'name',
            'num_products',
            'quantity',
            'stock_value'
        )
    )

    context = {
        "report_title": "Inventory Report",
        "generated_at": datetime.now(),
        "total_products": total_products,
        "total_quantity": total_quantity,
        "total_stock_value": total_stock_value,
        "low_stock_count": low_stock_count,
        "low_stock_threshold": LOW_STOCK_THRESHOLD,
        "products": products,
        "summary_by_category": summary_by_category,
    }

    return render(request, "products/inventory_report.html", context)

def supplier_report_view(request):
    LOW_STOCK_THRESHOLD = 5

    suppliers = (
        Supplier.objects
        .prefetch_related('products', 'products__category')
        .annotate(
            num_products=Count('products', distinct=True),
            total_quantity=Sum('products__quantity'),
            total_stock_value=Sum(F('products__price') * F('products__quantity')),
            low_stock_items=Count('products', filter=Q(products__quantity__lt=LOW_STOCK_THRESHOLD)),
        )
        .order_by('name')
    )

    totals = Product.objects.aggregate(
        total_products=Count('id'),
        total_quantity=Sum('quantity'),
        total_stock_value=Sum(F('price') * F('quantity')),
    )

    context = {
        "report_title": "Supplier Report",
        "generated_at": timezone.now(),
        "low_stock_threshold": LOW_STOCK_THRESHOLD,
        "total_suppliers": suppliers.count(),
        "total_products": totals.get('total_products') or 0,
        "total_quantity": totals.get('total_quantity') or 0,
        "total_stock_value": totals.get('total_stock_value') or 0,
        "suppliers": suppliers,
    }
    return render(request, "products/suppliers_report.html", context)

def import_products_csv(request):
    if request.method == 'POST' and 'file' in request.FILES:
        reader = csv.DictReader(request.FILES['file'].read().decode('utf-8').splitlines())
        default_image = static('images/No Image.png')
        for r in reader:
            cat, _ = Category.objects.get_or_create(name=r['category'])
            prod, _ = Product.objects.update_or_create(
                name=r['name'],
                defaults={
                    'description': r['description'],
                    'price': r['price'],
                    'quantity': r['quantity'],
                    'category': cat,
                    'image': r['image'] if r['image'] else default_image
                }
            )
            prod.suppliers.set(
                [Supplier.objects.get_or_create(name=s.strip())[0] for s in r['suppliers'].split('|') if s.strip()]
            )
        return redirect('products:display_all_products_view')
    return render(request, 'products/import_csv.html')


def export_products_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    writer.writerow(['name', 'description', 'price', 'quantity', 'category', 'suppliers', 'image'])

    for product in Product.objects.all():
        category = product.category.name if product.category else ''
        suppliers = '|'.join(s.name for s in product.suppliers.all())
        image_url = product.image.url if product.image else ''
        writer.writerow([
            product.name,
            product.description or '',
            product.price,
            product.quantity,
            category,
            suppliers,
            image_url
        ])

    return response
