from django.conf import settings
from django.db import models
from django.utils import timezone
from django.template.backends import django

if not settings.configured:
    settings.configure()


class Teams (models.Model):
    # team_id = models.IntegerField(primary_key=True)
    team_type = models.CharField(max_length=50)
    team_head_full_name = models.CharField(max_length=50)
    team_head_email = models.EmailField(max_length=50)
    open_tickets = models.IntegerField
    closed_tickets_month = models.IntegerField(default=0)
    closed_tickets_total = models.IntegerField(default=0)
    number_of_members = models.IntegerField(default=1)  # the team head is already in the team


class Employees (models.Model):
    employee_id = models.IntegerField(primary_key=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    department = models.CharField(max_length=50)
    tickets_closed_month = models.IntegerField(default=0)
    team_id = models.ForeignKey(Teams, on_delete=models.RESTRICT)


class EmployeesPrivateData(models.Model):
    employee_id = models.OneToOneField(Employees, primary_key=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=35)


class StatusOfTickets(models.TextChoices):
    assigned = 'ASSIGNED'
    in_progress = 'IN PROGRESS'
    lock = 'LOCK'
    done = 'DONE'
    dropped = 'DROPPED'


class ImportanceOfTickets(models.TextChoices):
    low = 'LOW'
    medium = 'MEDIUM'
    high = 'HIGH'
    critical = 'CRITICAL'
    dropped = 'DROPPED'


class Tickets (models.Model):
    ticket_id = models.IntegerField(primary_key=True)
    user_full_name = models.CharField(max_length=50)
    user_email = models.EmailField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    due_datetime = models.DateTimeField
    finish_at = models.DateTimeField
    status = models.CharField(max_length=50, choices=StatusOfTickets.choices, default=StatusOfTickets.assigned)
    importance = models.CharField(max_length=50, choices=ImportanceOfTickets.choices, default=ImportanceOfTickets.medium)
    responsible_team_id = models.ForeignKey(Teams, on_delete=models.RESTRICT)
    responsible_employee_id = models.ForeignKey(Employees, on_delete=models.RESTRICT)
    description = models.TextField


class Files(models.Model):
    file_id = models.IntegerField(primary_key=True)
    ticket_id = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    pdf_root = models.CharField(max_length=150)
    image_root = models.CharField(max_length=150)
    archive_root = models.CharField(max_length=150)


class Messages (models.Model):
    mes_id = models.IntegerField(primary_key=True)
    ticket_id = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    mes_form = models.EmailField(max_length=50)
    mes_to = models.EmailField(max_length=50)
    text = models.TextField(max_length=250)
    send_date = models.DateTimeField

