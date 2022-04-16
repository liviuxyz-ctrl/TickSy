# Generated by Django 4.0.3 on 2022-04-08 12:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('department', models.CharField(max_length=50)),
                ('tickets_closed_month', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=250)),
                ('team_head_full_name', models.CharField(max_length=50)),
                ('team_head_email', models.EmailField(max_length=50)),
                ('open_tickets', models.PositiveIntegerField(default=0)),
                ('closed_tickets_month', models.PositiveIntegerField(default=0)),
                ('closed_tickets_total', models.PositiveIntegerField(default=0)),
                ('number_of_members', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeesPrivateData',
            fields=[
                ('employee_id', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='ticketing.employees')),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=55)),
            ],
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_full_name', models.CharField(max_length=50)),
                ('user_email', models.EmailField(max_length=50)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('due_datetime', models.DateTimeField()),
                ('finish_at', models.DateTimeField()),
                ('status', models.CharField(choices=[('ASSIGNED', 'Assigned'), ('IN PROGRESS', 'In Progress'), ('LOCK', 'Lock'), ('DONE', 'Done'), ('DROPPED', 'Dropped')], default='ASSIGNED', max_length=50)),
                ('importance', models.CharField(choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')], default='MEDIUM', max_length=50)),
                ('responsible_employee_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='ticketing.employees')),
                ('responsible_team_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='ticketing.teams')),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes_form', models.EmailField(max_length=50)),
                ('mes_to', models.EmailField(max_length=50)),
                ('text', models.TextField(max_length=250)),
                ('send_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('ticket_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketing.tickets')),
            ],
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_root', models.CharField(max_length=150)),
                ('image_root', models.CharField(max_length=150)),
                ('archive_root', models.CharField(max_length=150)),
                ('ticket_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketing.tickets')),
            ],
        ),
        migrations.AddField(
            model_name='employees',
            name='team_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='ticketing.teams'),
        ),
    ]