# forms.py
from django import forms

class MachineSearchForm(forms.Form):
    machine_serial_number = forms.CharField(label="Заводской номер машины", max_length=50)