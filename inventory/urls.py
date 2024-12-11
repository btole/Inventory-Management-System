from django.contrib.auth import views as auth_views
from .views import SignUpView,Index,AddItemView, EditItemView, DeleteItemView,Dashboard,import_inventory, export_inventory,stock_summary_report,low_stock_report,inventory_movement_report
from django.urls import path

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('add-item/', AddItemView.as_view(), name='add-item'),
    path('edit-item/<int:pk>/', EditItemView.as_view(), name='edit-item'),
    path('delete-item/<int:pk>/', DeleteItemView.as_view(), name='delete-item'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('import-inventory/', import_inventory, name='import-inventory'),
    path('export-inventory/', export_inventory, name='export-inventory'),
    path('stock-summary-report/', stock_summary_report, name='stock-summary-report'),
    path('low-stock-report/', low_stock_report, name='low-stock-report'),
path('inventory-movement-report/', inventory_movement_report, name='inventory-movement-report')
]