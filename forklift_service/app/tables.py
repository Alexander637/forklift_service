# tables.py
import django_tables2 as tables
from .models import Machine, Maintenance, Complaint

class MachineTable(tables.Table):
    class Meta:
        model = Machine
        fields = [
            "machine_serial_number",
            "model_technique",
            "engine_model",
            "transmission_model",
            "drive_axle_model",
            "steering_axle_model",
            "shipment_date",
            "client",
            "service_company",
        ]
        order_by = "shipment_date"

class MaintenanceTable(tables.Table):
    class Meta:
        model = Maintenance
        fields = [
            "machine",
            "maintenance_type",
            "maintenance_date",
            "operating_hours",
            "performing_organization",
            "service_company",
        ]
        order_by = "maintenance_date"

class ComplaintTable(tables.Table):
    downtime = tables.Column(verbose_name="Простой (дни)")

    class Meta:
        model = Complaint
        fields = [
            "failure_date",
            "machine",
            "failure_node",
            "failure_description",
            "recovery_method",
            "spare_parts",
            "recovery_date",
            "downtime",
            "service_company",
        ]
        order_by = "failure_date"