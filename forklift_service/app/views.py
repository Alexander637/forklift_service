from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from .models import Machine, Maintenance, Complaint
from .tables import MachineTable, MaintenanceTable, ComplaintTable
from .filters import MachineFilter, MaintenanceFilter, ComplaintFilter
from .forms import MachineSearchForm
from django.template.loader import render_to_string
from django.http import JsonResponse

def home(request):
    return render(request, 'base.html')

def welcome_view(request):
    search_result = None
    if request.method == 'GET' and 'serial_number' in request.GET:
        serial_number = request.GET.get('serial_number')
        search_result = Machine.objects.filter(serial_number=serial_number)
    return render(request, 'welcome.html', {'search_result': search_result})

@login_required
def dashboard_view(request):
    machines = Machine.objects.all()
    maintenances = Maintenance.objects.all()
    complaints = Complaint.objects.all()
    
    return render(request, 'dashboard.html', {
        'machines': machines,
        'maintenances': maintenances,
        'complaints': complaints
    })


def search_machine_view(request):
    form = MachineSearchForm()
    search_results = None

    if request.method == "GET" and request.GET.get("serial_number"):
        serial_number = request.GET.get("serial_number")
        machine = Machine.objects.filter(machine_serial_number=serial_number).first()

        if machine:
            search_results = {
                "Зав. № машины": machine.machine_serial_number,
                "Модель техники": machine.model_technique.name,
                "Модель двигателя": machine.engine_model.name,
                "Дата отгрузки": machine.shipment_date,
            }
        else:
            search_results = {"Ошибка": "Машина с таким заводским номером не найдена."}

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            html = render_to_string(
                "partials/search_results.html", {"search_results": search_results}
            )
            return JsonResponse({"html": html})

    return render(request, "welcome.html", {"form": form, "search_results": search_results})


class MachineListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Machine
    table_class = MachineTable
    template_name = "table_view.html"
    filterset_class = MachineFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Machine.objects.all()
        elif user.groups.filter(name="Клиенты").exists():
            return Machine.objects.filter(client=user)
        elif user.groups.filter(name="Сервисные компании").exists():
            return Machine.objects.filter(service_company=user)
        return Machine.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name_plural'] = self.model._meta.verbose_name_plural
        return context

class MaintenanceListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Maintenance
    table_class = MaintenanceTable
    template_name = "table_view.html"
    filterset_class = MaintenanceFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Maintenance.objects.all()
        elif user.groups.filter(name="Сервисные компании").exists():
            return Maintenance.objects.filter(service_company=user)
        return Maintenance.objects.none()

class ComplaintListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Complaint
    table_class = ComplaintTable
    template_name = "table_view.html"
    filterset_class = ComplaintFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Complaint.objects.all()
        elif user.groups.filter(name="Сервисные компании").exists():
            return Complaint.objects.filter(service_company=user)
        return Complaint.objects.none()