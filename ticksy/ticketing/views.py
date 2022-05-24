import logging

from .models import Employees, Teams, EmployeesPrivateData, Tickets
from .serializers import EmployeesSerializer, UserSerializer, TeamSerializer
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

logger = logging.getLogger("API Logger")


def set_login_state_session(request, user_email: str):
    logger.info(f"Setting user session with user_email '{user_email}'!")
    request.session['login_state'] = True
    request.session['user_email'] = user_email


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')


def about_us(request):
    if request.method == 'GET':
        return render(request, 'about-us.html')


def tickets_creator(request):
    if request.method == 'GET':
        return render(request, 'tickets_creator.html')


def tickets_list(request):
    if request.method == 'GET':
        return render(request, 'tickets_list.html')


def contact_page(request):
    if request.method == 'GET':
        return render(request, 'contact-us.html')


@api_view(['GET', 'POST'])
def login(request, logout_user=False):
    login_api_response = {
        'login_deny': False,
        'email_exists': False,
        'successful_pwd_match': False,
        'successful_login': False
    }
    post_header_data_validation_list = ['login_email', 'login_password']

    if not request.session.get('login_state', default=False):

        if request.method == 'GET':
            # Display login page
            if not request.session.get('login_state', default=False):
                return render(request, 'login.html')
            else:
                if settings.ENABLE_REST_FRAMEWORK_RESPONSE:
                    return Response(data=login_api_response)
                else:
                    return JsonResponse(data=login_api_response)

        if request.method == 'POST':
            for required_post_header_key in post_header_data_validation_list:
                if required_post_header_key not in request.data.keys():
                    logger.critical("Malformed HTTP POST request, missing form keys!")
                    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
            try:
                employee_entry = EmployeesPrivateData.objects.get(email=request.data['login_email'])
            except ObjectDoesNotExist:
                if settings.ENABLE_REST_FRAMEWORK_RESPONSE:
                    return Response(data=login_api_response)
                else:
                    return JsonResponse(data=login_api_response)
            login_api_response['email_exists'] = True
            if check_password(request.data['login_password'], employee_entry.password):
                login_api_response['successful_pwd_match'] = True
                try:
                    set_login_state_session(request, request.data['login_email'])
                    login_api_response['successful_login'] = True
                except:
                    login_api_response['successful_login'] = False
            else:
                login_api_response['successful_pwd_match'] = False
            if settings.ENABLE_REST_FRAMEWORK_RESPONSE:
                return Response(data=login_api_response)
            else:
                return JsonResponse(data=login_api_response)
    else:
        # Logout flag set
        if logout_user:
            return logout(request)
        # Login deny
        logger.debug(f"Login deny, user '{request.session['user_email']}' already logged in!")
        login_api_response['login_deny'] = True
        login_api_response['email_exists'] = None
        login_api_response['successful_pwd_match'] = None
        login_api_response['successful_login'] = None
        if settings.ENABLE_REST_FRAMEWORK_RESPONSE:
            return Response(data=login_api_response)
        else:
            return JsonResponse(data=login_api_response)


def logout(request):
    if request.method == 'GET':
        if request.session.get('login_state', default=False):
            logger.info(f"Logging out user with email '{request.session['user_email']}'!")
            request.session.clear()
    return HttpResponseRedirect('/login/')


def register_error_validation(serializer_object, api_response, api_response_key='validator_error_messages'):
    if not serializer_object.is_valid():
        sanitized_error_data = {}
        for key, values in serializer_object.errors.items():
            sanitized_error_data[key] = [{'message': value[:], 'code': value.code} for value in values]
        api_response[api_response_key] = sanitized_error_data
        logger.error(f"Validation failed for '{type(serializer_object)}', returning error in API response!")
        return Response(data=api_response)
    logger.info(f"Validation successful for '{type(serializer_object)}'!")
    return False


@api_view(['GET', 'POST'])
def register(request):
    register_api_response = {
        'register_deny': False,
        'successful_registration': False,
        'validator_error_messages': []
    }
    post_header_data_validation_list = ['register_fullname', 'register_email', 'register_department',
                                        'register_password', 'register_repassword', 'register_team_name', ]

    if not request.session.get('login_state', default=False):

        if request.method == 'GET':
            # Display register page
            return render(request, 'register.html')

        if request.method == 'POST':
            for required_post_header_key in post_header_data_validation_list:
                if required_post_header_key not in request.data.keys():
                    logger.critical("Malformed HTTP POST request, missing form keys!")
                    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

            sanitized_employee_data = {'full_name': request.data['register_fullname'],
                                       'email': request.data['register_email'],
                                       'department': request.data['register_department'],
                                       'team_name': request.data['register_team_name']
                                       }
            employee = EmployeesSerializer(data=sanitized_employee_data)
            response_obj = register_error_validation(employee, register_api_response)
            if response_obj:
                return response_obj
            employee_obj = employee.save()
            if employee_obj is None:
                logger.critical("Failed to generate Employee, aborting registration!")
                return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            sanitized_employee_private_data = {
                'employee_id': employee_obj.pk,
                'password': request.data['register_password'],
                're_password': request.data['register_repassword'],
                'email': employee.validated_data['email']
            }
            employee_private_data = UserSerializer(data=sanitized_employee_private_data)
            response_obj = register_error_validation(employee_private_data, register_api_response)
            try:
                if response_obj:
                    logger.critical("Failed to generate EmployeePrivateData, deleting Employee record from database!")
                    employee_obj.delete()
                    return response_obj
                employee_private_data_obj = employee_private_data.save()
                if employee_private_data_obj is None:
                    employee_obj.delete()
                    logger.critical("Failed to generate EmployeePrivateData, deleting Employee record from database!")
                    return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except:
                logger.critical("Failed to generate EmployeePrivateData, deleting Employee record from database!")
                employee_obj.delete()
                return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            logger.info(f"Registration successful for user with email '{sanitized_employee_private_data['email']}'!")
            register_api_response['successful_registration'] = True
            set_login_state_session(request, employee_private_data.validated_data['email'])
            return Response(data=register_api_response)
    else:
        logger.debug(f"Register deny, user '{request.session['user_email']}' already logged in!")
        register_api_response['register_deny'] = True
        register_api_response['successful_registration'] = None
        register_api_response['validator_error_messages'] = None
        return Response(data=register_api_response)


@api_view(['GET', 'POST'])
def register_team(request):
    register_team_api_response = {
        'team_register_deny': False,
        'team_successful_registration': False,
        'validator_error_messages': []
    }
    post_header_data_validation_list = ['register_team_name', 'register_team_head_full_name']

    if request.session.get('login_state', default=False):

        if request.method == 'GET':
            # Display register page
            return render(request, 'team.html')

        if request.method == 'POST':
            for required_post_header_key in post_header_data_validation_list:
                if required_post_header_key not in request.data.keys():
                    logger.critical("Malformed HTTP POST request, missing form keys!")
                    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

            sanitized_team_data = {'team_name': request.data['register_team_name'],
                                   'team_head_full_name': request.data['register_team_head_full_name'],
                                   'team_head_email': request.session['user_email'],
                                   }
            team = TeamSerializer(data=sanitized_team_data)
            response_obj = register_error_validation(team, register_team_api_response)
            if response_obj:
                return response_obj
            team_obj = team.save()
            if team_obj is None:
                logger.critical("Failed to generate Team, aborting team registration!")
                return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            logger.info(f"Registration successful for team with name '{sanitized_team_data['team_name']}'!")
            register_team_api_response['team_successful_registration'] = True
            return Response(data=register_team_api_response)
    else:
        logger.debug(f"Team register deny, user not logged in!")
        register_team_api_response['team_register_deny'] = True
        register_team_api_response['team_successful_registration'] = None
        register_team_api_response['validator_error_messages'] = None
        return Response(data=register_team_api_response)


@api_view(['GET'])
def lookup_team(request, team_name):
    lookup_team_api_response = {
        'team_lookup_deny': False,
        'team_successful_lookup': False,
        'team_object_found': False,
        'team_lookup_object': None
    }

    if request.session.get('login_state', default=False):
        if request.method == 'GET':
            try:
                team = Teams.objects.get(team_name=team_name)
            except ObjectDoesNotExist:
                logger.info(f"Team with name '{team_name}' requested by user '{request.session['user_email']}' does "
                            f"not exist!")
            else:
                logger.info(f"Team with name '{team_name}' requested by user '{request.session['user_email']}' was "
                            f"found, serializing object!")
                lookup_team_api_response['team_object_found'] = True
                team_serializer = TeamSerializer(data=model_to_dict(team), disable_team_name_validation=True)
                response_obj = register_error_validation(team_serializer, lookup_team_api_response, 'team_lookup_object'
                                                         )
                if response_obj:
                    logger.info(f"TeamSerializer validator received malformed data, removing team entry from database!")
                    team.delete()
                    return response_obj
                lookup_team_api_response['team_lookup_object'] = team_serializer.validated_data

            logger.info(f"Team lookup operation requested by user '{request.session['user_email']}' was successful!")
            lookup_team_api_response['team_successful_lookup'] = True
            return Response(data=lookup_team_api_response)
    else:
        logger.debug(f"Team lookup deny, user not logged in!")
        lookup_team_api_response['team_lookup_deny'] = True
        lookup_team_api_response['team_successful_lookup'] = None
        lookup_team_api_response['team_object_found'] = None
        lookup_team_api_response['team_lookup_object'] = None
        return Response(data=lookup_team_api_response)


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
