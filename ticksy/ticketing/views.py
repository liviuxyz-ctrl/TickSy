from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .serializers import EmployeesSerializer,TeamSerializer
from .models import Employees,Teams,EmployeesPrivateData,Tickets
# from .forms import RegisterEmployeeForm,CreateTeamForm
from django.contrib.auth.hashers import make_password

def test(request):
    return render(request, 'test.html')
    # return HttpResponse('test')

def login(request):
    if request.method == 'POST' and request.POST.get("login"):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            try:
                e = Employees.objects.get(email=email)
                if e.password == make_password(password):
                    return render(request, 'test.html')
            except:
                return render(request,'login.html', {'unkonform data':True})
    return render(request, 'login.html')


def register(request):
    if request.method == 'GET':
        # return render(request, 'register.html')
        print('get in register')
        return render(request, 'register.html')
    if request.method == 'POST' and request.POST.get("register"):
        full_name = request.POST.get('fullname')
        email = request.POST.get('email')
        department  = request.POST.get('department')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        team_name = request.POST.get('teamname')
        if full_name and email and department and password and repassword and team_name:
            # try:
                if password != repassword:
                    return render(request, 'register.html',{'password_dont_mach':True})
                e = Employees()
                e.full_name = full_name
                e.email = email
                e.department = department
                e.team_id = Teams.objects.get(team_name=team_name)

                ep = EmployeesPrivateData()
                ep.email = email
                ep.password = make_password(password)
                ep.employee_id = e

                e.save()
                ep.save()
                # except IntegrityError:
                #     return render(request, 'test.html','Email already in use')
                print('ok')
                return render(request, 'login.html')
    return render(request, 'register.html')


def team(request):
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        team_head_name = request.POST.get('team_head_name')
        team_head_email = request.POST.get('team_head_email')
        if team_name and team_head_name and team_head_email:
            team = Teams()
            team.team_name=team_name
            team.team_head_full_name=team_head_name
            team.team_head_email=team_head_email
            team.save()
            return render(request, 'test.html')
    return render(request, 'team.html')


def ticket(request):
    if request.method == 'POST':

        fromNameT = request.POST.get('fromname')
        fromEmailT = request.POST.get('fromemail')
        toT = request.POST.get('to')
        descriptionT = request.POST.get('description')
        priorityT = request.POST.get('priority')
        teamT = request.POST.get('team')
        domainT = request.POST.get('domain')
        deadlineT = request.POST.get('deadline')

        if fromNameT and fromEmailT and toT and descriptionT and priorityT and teamT and domainT and deadlineT:
            ticket = Tickets()
            ticket.user_full_name = fromNameT
            ticket.user_email = fromEmailT
            ticket.responsible_team_id = Teams.objects.get(team_name=teamT)
            ticket.responsible_employee_id = Employees.objects.get(full_name=toT)
            ticket.description = descriptionT
            ticket.due_datetime = deadlineT

            ticket.save()
            return render(request, 'test.html')
    return render(request, 'ticket.html')


# user_full_name = models.CharField(max_length=50)
#     user_email = models.EmailField(max_length=50)
#     created_at = models.DateTimeField(default=timezone.now)
#     due_datetime = models.DateTimeField()
#     finish_at = models.DateTimeField()
#     status = models.CharField(max_length=50, choices=StatusOfTickets.choices, default=StatusOfTickets.assigned)
#     importance = models.CharField(max_length=50, choices=ImportanceOfTickets.choices, default=ImportanceOfTickets.medium)
#     responsible_team_id = models.ForeignKey(Teams, on_delete=models.RESTRICT)
#     responsible_employee_id = models.ForeignKey(Employees, on_delete=models.RESTRICT)
#     description = models.TextField(default="empty")


# def team(request):
#     if request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = TeamSerializer(data = data)
#         # serializer.update(data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.erors, status=400)
#     return render(request, 'team.html')

# def register(request):
#     if request.method == 'POST':
#         data = JSONParser().parse(request)
#         seroalizer = EmployeesSerializer(data = data)
#         seroalizer.update(data)







    #     if request.POST.get('name') and request.POST.get('email') and request.POST.get('department'):
    #         e = Employees()
    #         e.full_name = request.POST.get('name')
    #         e.email = request.POST.get('email')
    #         e.department = request.POST.get('department')
    #         e.team_id = Teams.objects.get(id=1)
    #         e.save()
    #         return render(request, 'test.html')
    #     else:
    #         return render(request, 'register.html')
    # else:
    #     return render(request, 'register.html')
    #cleaned_data

def index(request):
        submitbutton = request.POST.get('Register')
        print(submitbutton)
        if submitbutton: # execute this code
            context = {'submitbutton': submitbutton}
            return render(request, 'test.html')

        return render(request, 'index.html')

def contact(reqest):
    return render(reqest, 'contact.html')