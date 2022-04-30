from django.contrib import admin
from .models import EmployeesPrivateData, Employees, Teams, Tickets

admin.site.register(Employees)
admin.site.register(EmployeesPrivateData)
admin.site.register(Teams)
admin.site.register(Tickets)
