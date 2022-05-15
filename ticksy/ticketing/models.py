from django.conf import settings
from django.db import models
from django.utils import timezone

if not settings.configured:
    settings.configure()


class Teams (models.Model):
    team_name = models.CharField(max_length=250)
    team_head_full_name = models.CharField(max_length=50)
    team_head_email = models.EmailField(max_length=50)
    open_tickets = models.PositiveIntegerField(default=0)
    closed_tickets_month = models.PositiveIntegerField(default=0)
    closed_tickets_total = models.PositiveIntegerField(default=0)
    number_of_members = models.PositiveIntegerField(default=1)  # the team head is already in the team


class Employees (models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    department = models.CharField(max_length=50)
    team_id = models.ForeignKey(Teams, on_delete=models.RESTRICT)
    tickets_closed_month = models.PositiveIntegerField(default=0)


class EmployeesPrivateData(models.Model):
    employee_id = models.OneToOneField(Employees, primary_key=True, on_delete=models.CASCADE, auto_created=True)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=100)


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


class Tickets (models.Model):
    user_full_name = models.CharField(max_length=50)
    user_email = models.EmailField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    due_datetime = models.DateTimeField()
    finish_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=50, choices=StatusOfTickets.choices, default=StatusOfTickets.assigned)
    importance = models.CharField(max_length=50, choices=ImportanceOfTickets.choices, default=ImportanceOfTickets.medium)
    responsible_team_id = models.ForeignKey(Teams, on_delete=models.RESTRICT)
    responsible_employee_id = models.ForeignKey(Employees, on_delete=models.RESTRICT)
    description = models.TextField(default="empty")


class Files(models.Model):
    ticket_id = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    pdf_root = models.FileField(upload_to='pdfs/',null=True)
    image_root = models.FileField(upload_to='images/',null=True)
    archive_root = models.FileField(upload_to='archives/', null=True)


class Messages (models.Model):
    ticket_id = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    mes_form = models.EmailField(max_length=50)
    mes_to = models.EmailField(max_length=50)
    text = models.TextField(max_length=500)
    send_date = models.DateTimeField(default=timezone.now)

