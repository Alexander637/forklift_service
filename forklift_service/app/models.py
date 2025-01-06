from django.db import models
from django.contrib.auth.models import User

class Reference(models.Model):
    entity_name = models.CharField(max_length=100, verbose_name="Название сущности")
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    def __str__(self):
        return f"{self.entity_name}: {self.name}"

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"
        indexes = [models.Index(fields=["entity_name", "name"])]

class Machine(models.Model):
    machine_serial_number = models.CharField(max_length=50, unique=True, verbose_name="Зав. № машины")
    model_technique = models.ForeignKey(Reference, on_delete=models.PROTECT, limit_choices_to={'entity_name': 'Модель техники'}, related_name="machines_with_model_technique", verbose_name="Модель техники")
    engine_model = models.ForeignKey(Reference, on_delete=models.PROTECT, limit_choices_to={'entity_name': 'Модель двигателя'}, related_name="machines_with_engine_model", verbose_name="Модель двигателя")
    engine_serial_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Зав. № двигателя")
    transmission_model = models.ForeignKey(Reference, on_delete=models.PROTECT, limit_choices_to={'entity_name': 'Модель трансмиссии'}, related_name="machines_with_transmission_model", verbose_name="Модель трансмиссии")
    transmission_serial_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Зав. № трансмиссии")
    drive_axle_model = models.ForeignKey(Reference, on_delete=models.PROTECT, limit_choices_to={'entity_name': 'Модель ведущего моста'}, related_name="machines_with_drive_axle_model", verbose_name="Модель ведущего моста")
    drive_axle_serial_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Зав. № ведущего моста")
    steering_axle_model = models.ForeignKey(Reference, on_delete=models.PROTECT, limit_choices_to={'entity_name': 'Модель управляемого моста'}, related_name="machines_with_steering_axle_model", verbose_name="Модель управляемого моста")
    steering_axle_serial_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Зав. № управляемого моста")
    supply_contract = models.TextField(blank=True, null=True, verbose_name="Договор поставки №, дата")
    shipment_date = models.DateField(blank=True, null=True, verbose_name="Дата отгрузки с завода")
    consignee = models.CharField(max_length=200, blank=True, null=True, verbose_name="Грузополучатель (конечный потребитель)")
    delivery_address = models.CharField(max_length=300, blank=True, null=True, verbose_name="Адрес поставки (эксплуатации)")
    additional_options = models.TextField(blank=True, null=True, verbose_name="Комплектация (доп. опции)")
    client = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='client_machines', blank=True, null=True, verbose_name="Клиент")
    service_company = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='service_machines', blank=True, null=True, verbose_name="Сервисная компания")

    def __str__(self):
        return self.machine_serial_number

class Maintenance(models.Model):
    maintenance_type = models.ForeignKey(Reference, on_delete=models.PROTECT, limit_choices_to={'entity_name': 'Вид ТО'}, related_name="maintenances_of_type", verbose_name="Вид ТО")
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='maintenances', verbose_name="Машина")
    maintenance_date = models.DateField(verbose_name="Дата проведения ТО")
    operating_hours = models.PositiveIntegerField(blank=True, null=True, verbose_name="Наработка, м/час")
    order_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="№ заказ-наряда")
    order_date = models.DateField(blank=True, null=True, verbose_name="Дата заказ-наряда")
    performing_organization = models.ForeignKey(Reference, on_delete=models.PROTECT, limit_choices_to={'entity_name': 'Организация, проводившая ТО'}, related_name="maintenances_by_organization", verbose_name="Организация, проводившая ТО")
    service_company = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='maintenances_by_service_company', blank=True, null=True, verbose_name="Сервисная компания")

    def __str__(self):
        return f"{self.maintenance_type.name} для {self.machine.machine_serial_number} ({self.maintenance_date})"

class Complaint(models.Model):
    failure_date = models.DateField(verbose_name="Дата отказа")
    operating_hours = models.PositiveIntegerField(blank=True, null=True, verbose_name="Наработка, м/час")
    failure_node = models.ForeignKey(Reference, on_delete=models.PROTECT, limit_choices_to={'entity_name': 'Узел отказа'}, related_name="complaints_with_failure_node", verbose_name="Узел отказа")
    failure_description = models.TextField(blank=True, null=True, verbose_name="Описание отказа")
    recovery_method = models.ForeignKey(Reference, on_delete=models.PROTECT, limit_choices_to={'entity_name': 'Способ восстановления'}, related_name="complaints_with_recovery_method", verbose_name="Способ восстановления")
    spare_parts = models.TextField(blank=True, null=True, verbose_name="Используемые запасные части")
    recovery_date = models.DateField(blank=True, null=True, verbose_name="Дата восстановления")
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='complaints', verbose_name="Машина")
    service_company = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='complaints_by_service_company', blank=True, null=True, verbose_name="Сервисная компания")

    @property
    def downtime(self):
        if self.failure_date and self.recovery_date:
            return (self.recovery_date - self.failure_date).days
        return None

    def __str__(self):
        return f"Рекламация {self.failure_node.name} для {self.machine.machine_serial_number} от {self.failure_date}"