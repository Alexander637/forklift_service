from django.contrib import admin
from .models import Machine, Maintenance, Complaint, Reference

class MaintenanceInline(admin.TabularInline):
    model = Maintenance
    extra = 1

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = (
        'machine_serial_number', 
        'get_model_technique_name',
        'shipment_date', 
        'client', 
        'service_company'
    )
    search_fields = ('machine_serial_number', 'client__username', 'service_company__username')
    inlines = [MaintenanceInline]

    def get_model_technique_name(self, obj):
        return obj.model_technique.name
    get_model_technique_name.short_description = "Модель техники"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not request.user.is_authenticated:
            queryset = queryset.only('machine_serial_number', 'shipment_date', 'client', 'service_company')

        elif request.user.groups.filter(name='client').exists():
            queryset = queryset.filter(client=request.user)

        elif request.user.groups.filter(name='service_company').exists():
            queryset = queryset.filter(service_company=request.user)

        elif request.user.groups.filter(name='manager').exists():
            pass  
        
        return queryset

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('maintenance_type', 'maintenance_date', 'machine', 'performing_organization', 'service_company')
    search_fields = ('maintenance_type__name', 'machine__machine_serial_number', 'performing_organization__name')
    list_filter = ('maintenance_date', 'performing_organization__name')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.groups.filter(name='client').exists():
            queryset = queryset.filter(machine__client=request.user)

        elif request.user.groups.filter(name='service_company').exists():
            queryset = queryset.filter(machine__service_company=request.user)

        elif request.user.groups.filter(name='manager').exists():
            pass
        
        return queryset

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('failure_date', 'machine', 'failure_node', 'recovery_date', 'downtime', 'service_company')
    search_fields = ('machine__machine_serial_number', 'failure_node__name', 'service_company__username')
    list_filter = ('failure_date', 'recovery_date', 'service_company')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.groups.filter(name='client').exists():
            queryset = queryset.filter(machine__client=request.user)

        elif request.user.groups.filter(name='service_company').exists():
            queryset = queryset.filter(machine__service_company=request.user)

        elif request.user.groups.filter(name='manager').exists():
            pass
        
        return queryset

@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ("entity_name", "name", "description")
    list_filter = ("entity_name",)
    search_fields = ("entity_name", "name")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.groups.filter(name='manager').exists():
            return queryset
        
        return queryset
    