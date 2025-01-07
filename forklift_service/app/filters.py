# filters.py
import django_filters
from .models import Machine, Maintenance, Complaint, Reference

class MachineFilter(django_filters.FilterSet):
    model_technique = django_filters.ModelChoiceFilter(
        queryset=Reference.objects.filter(entity_name="Модель техники")
    )
    engine_model = django_filters.ModelChoiceFilter(
        queryset=Reference.objects.filter(entity_name="Модель двигателя")
    )
    transmission_model = django_filters.ModelChoiceFilter(
        queryset=Reference.objects.filter(entity_name="Модель трансмиссии")
    )
    drive_axle_model = django_filters.ModelChoiceFilter(
        queryset=Reference.objects.filter(entity_name="Модель ведущего моста")
    )
    steering_axle_model = django_filters.ModelChoiceFilter(
        queryset=Reference.objects.filter(entity_name="Модель управляемого моста")
    )

    class Meta:
        model = Machine
        fields = [
            "model_technique",
            "engine_model",
            "transmission_model",
            "drive_axle_model",
            "steering_axle_model"
        ]

class MaintenanceFilter(django_filters.FilterSet):
    maintenance_type = django_filters.ModelChoiceFilter(
        queryset=Reference.objects.filter(entity_name="Maintenance type")
    )
        
    class Meta:
        model = Maintenance
        fields = {
            "maintenance_type",
            "machine__machine_serial_number",
            "service_company",
        }

class ComplaintFilter(django_filters.FilterSet):
    failure_node = django_filters.ModelChoiceFilter(
        queryset=Reference.objects.filter(entity_name="Failure node")
    )
    recovery_method = django_filters.ModelChoiceFilter(
        queryset=Reference.objects.filter(entity_name="Recovery method")
    )
    class Meta:
        model = Complaint
        fields = {
            "failure_node": ["exact"],
            "recovery_method": ["exact"],
            "service_company": ["exact"],
        }
        