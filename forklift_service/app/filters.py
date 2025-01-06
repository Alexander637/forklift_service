# filters.py
import django_filters
from .models import Machine, Maintenance, Complaint

class MachineFilter(django_filters.FilterSet):
    class Meta:
        model = Machine
        fields = {
            "model_technique": ["exact"],
            "engine_model": ["exact"],
            "transmission_model": ["exact"],
            "drive_axle_model": ["exact"],
            "steering_axle_model": ["exact"],
        }

class MaintenanceFilter(django_filters.FilterSet):
    class Meta:
        model = Maintenance
        fields = {
            "maintenance_type": ["exact"],
            "machine__machine_serial_number": ["icontains"],
            "service_company": ["exact"],
        }

class ComplaintFilter(django_filters.FilterSet):
    class Meta:
        model = Complaint
        fields = {
            "failure_node": ["exact"],
            "recovery_method": ["exact"],
            "service_company": ["exact"],
        }
        