import csv
from django.db import models
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from .forms import UserRegisterForm
from django.views.generic import TemplateView
from django.views.generic import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import InventoryItems,Category,StockMovement
from .forms import InventoryItemForm
from inventory_management.settings import LOW_QUANTITY
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Sum
# Create your views here.


class Index(TemplateView):
    template_name = 'index.html'
class SignUpView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        return render(request, 'signup.html', {'form': form})

class AddItemView(LoginRequiredMixin, CreateView):
    model = InventoryItems
    form_class = InventoryItemForm
    template_name = 'item_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EditItemView(LoginRequiredMixin, UpdateView):
    model = InventoryItems
    form_class = InventoryItemForm
    template_name = 'item_form.html'
    success_url = reverse_lazy('dashboard')

class DeleteItemView(LoginRequiredMixin, DeleteView):
    model = InventoryItems
    template_name = 'delete_item.html'
    success_url = reverse_lazy('dashboard')

class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        # Get search query and filter parameters
        search_query = request.GET.get('search', '')
        category_filter = request.GET.get('category', '')
        low_stock_filter = request.GET.get('low_stock', False)

        # Base query for inventory items for the logged-in user
        items = InventoryItems.objects.filter(user=request.user)

        # Apply search filter (search by item name)
        if search_query:
            items = items.filter(name__icontains=search_query)

        # Apply category filter
        if category_filter:
            items = items.filter(category__id=category_filter)

        # Apply low-stock filter
        if low_stock_filter:
            items = items.filter(quantity__lte=LOW_QUANTITY)

        # Identify low-stock items for message display
        low_inventory = items.filter(quantity__lte=LOW_QUANTITY)
        low_inventory_count = low_inventory.count()

        # Add a message for low inventory
        if low_inventory_count > 0:
            item_word = "item" if low_inventory_count == 1 else "items"
            messages.warning(request, f"{low_inventory_count} {item_word} have low inventory.")

        # Fetch all categories for filtering
        categories = Category.objects.all()

        # Prepare context for the template
        context = {
            'items': items,
            'low_inventory': low_inventory,
            'categories': categories,
            'search_query': search_query,
            'category_filter': category_filter,
            'low_stock_filter': low_stock_filter
        }

        return render(request, 'dashboard.html', context)

def import_inventory(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']

        # Check if the uploaded file is a CSV
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Please upload a valid CSV file.")
            return redirect('import-inventory')

        # Process CSV file
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)

        # Skip header row
        next(reader)

        for row in reader:
            try:
                # Expect columns: name, quantity, category_name
                name, quantity, category_name = row
                category, created = Category.objects.get_or_create(name=category_name)
                InventoryItems.objects.create(
                    name=name,
                    quantity=int(quantity),
                    category=category
                )
            except Exception as e:
                messages.error(request, f"Error importing row {row}: {str(e)}")
                continue

        messages.success(request, "Inventory imported successfully.")
        return redirect('dashboard')

    return render(request, 'import_inventory.html')
def export_inventory(request):
    # Create the response object for CSV file download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Quantity', 'Category', 'Date Created'])

    # Fetch all inventory items and write them to the CSV
    inventory_items = InventoryItems.objects.all()
    for item in inventory_items:
        writer.writerow([item.name, item.quantity, item.category.name, item.date_created])

    return response
def stock_summary_report(request):
    # Aggregate inventory items by category to get the total quantity
    summary = InventoryItems.objects.values('category__name') \
        .annotate(total_quantity=models.Sum('quantity')) \
        .order_by('category__name')

    return render(request, 'stock_summary_report.html', {'summary': summary})
def low_stock_report(request):
    # Get all items with quantity less than or equal to LOW_QUANTITY
    low_stock_items = InventoryItems.objects.filter(quantity__lte=LOW_QUANTITY)
    return render(request, 'low_stock_report.html', {'low_stock_items': low_stock_items})
def inventory_movement_report(request):
    # Fetch stock movements
    movements = StockMovement.objects.all().order_by('-date')
    return render(request, 'inventory_movement_report.html', {'movements': movements})
# class AdminRequiredMixin(UserPassesTestMixin):
#     def test_func(self):
#         return self.request.user.groups.filter(name='Admin').exists()

# class Dashboard(LoginRequiredMixin, AdminRequiredMixin, View):
#     def get(self, request):
#         # Only users in the Admin group can access this view
#         return render(request, 'dashboard.html')
#
# class ManagerRequiredMixin(UserPassesTestMixin):
#     def test_func(self):
#         return self.request.user.groups.filter(name='Manager').exists()
#
# class ManagerDashboard(LoginRequiredMixin, ManagerRequiredMixin, View):
#     def get(self, request):
#         # Only users in the Manager group can access this view
#         return render(request, 'manager_dashboard.html')