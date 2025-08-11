from django.urls import path
from . import views


app_name = "products"

urlpatterns = [
    path('add_product/', views.add_product_view , name="add_product_view"),
    path('add_supplier/', views.add_supplier_view , name="add_supplier_view"),
    path('admin_supplier/', views.admin_supplier_view , name="admin_supplier_view"),
    path('supplier/<int:supplier_id>/', views.supplier_detail_view, name="supplier_detail_view"),  
    path('update_supplier/<int:supplier_id>/', views.update_supplier_view, name="update_supplier_view"),
    path('delete_supplier/<int:supplier_id>/', views.delete_supplier_view, name="delete_supplier_view"),
    path('display_all_suppliers/', views.display_all_suppliers_view, name="display_all_suppliers_view"),
    path('add_category/', views.add_category_view , name="add_category_view"),
    path('category/<int:category_id>/', views.category_detail_view, name="category_detail_view"),
    path('admin_category/', views.admin_category_view, name="admin_category_view"),
    path('update_category/<int:category_id>/', views.update_category_view, name="update_category_view"),
    path('delete_category/<int:category_id>/', views.delete_category_view, name="delete_category_view"),
    path('display_all_categories/', views.display_all_categories_view, name='display_all_categories_view'),
    path('admin_product/', views.admin_product_view, name='admin_product_view'),
    path('display_all_products/', views.display_all_products_view, name='display_all_products_view'),
    path('product_detail/<int:product_id>/', views.product_detail_view, name='product_detail_view'),
    path('update/product/<int:product_id>/', views.update_product_view, name='update_product_view'),
    path('delete/product/<int:product_id>/', views.delete_product_view, name='delete_product_view'),
    path('search/', views.search_products_view, name='search_products_view'),
    path("inventory/report/", views.inventory_report_view, name="inventory_report_view"),
    path("suppliers/report/", views.supplier_report_view, name="supplier_report_view"),
    path('import-csv/', views.import_products_csv, name='import_products_csv'),
    path('export-csv/', views.export_products_csv, name='export_products_csv'),


]