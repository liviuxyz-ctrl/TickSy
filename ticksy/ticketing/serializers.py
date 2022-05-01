from .models import Employees, EmployeesPrivateData, Teams
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.password_validation import validate_password, get_default_password_validators
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=100)

    class Meta:
        model = EmployeesPrivateData
        fields = ['employee_id', 'email', 'password', 're_password']
        extra_kwargs = {
            'email': {
                'validators': [],
            }
        }

    @classmethod
    def validate_password(cls, value):
        # Raise ValidationError if default password validator fails
        validate_password(password=value,
                          password_validators=get_default_password_validators())
        return value

    def validate_re_password(self, value):
        password = self.get_initial().get('password')
        if password != value:
            raise ValidationError("Passwords do not match.", code='passwords_mismatch')
        return value

    def create(self, validated_data):
        if 're_password' in validated_data:
            del validated_data['re_password']
            validated_data['password'] = make_password(validated_data['password'])
            return EmployeesPrivateData.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.employee_id = validated_data.get('employee_id', instance.employee_id)
        instance.email = validated_data.get('email', instance.email)
        instance.password = make_password(validated_data.get('password', instance.password))
        instance.save()


class EmployeesSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(max_length=256)

    class Meta:
        model = Employees
        fields = ['id', 'full_name', 'email', 'department', 'team_name']

    @classmethod
    def validate_team_name(cls, value):
        try:
            Teams.objects.get(team_name=value)
        except ObjectDoesNotExist:
            raise ValidationError("Team does not exist.", code='team_does_not_exist')
        return value

    def create(self, validated_data):
        if 'team_id' not in validated_data and 'team_name' in validated_data:
            validated_data['team_id'] = Teams.objects.get(team_name=validated_data['team_name'])
            del validated_data['team_name']
            return Employees.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('fullname', instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.department = validated_data.get('department', instance.department)
        instance.team_name = validated_data.get('team_name', instance.team)
        instance.save()


class TeamSerializer(serializers.ModelSerializer):
    disable_team_name_validation = False

    class Meta:
        model = Teams
        fields = ['team_name', 'team_head_full_name', 'team_head_email', 'open_tickets', 'closed_tickets_month',
                  'number_of_members']

    def __init__(self, disable_team_name_validation=False, **kwargs):
        if 'disable_team_name_validation' in kwargs:
            del kwargs['disable_team_name_validation']
        self.disable_team_name_validation = disable_team_name_validation
        super().__init__(**kwargs)

    def validate_team_name(self, value):
        if not self.disable_team_name_validation:
            try:
                Teams.objects.get(team_name=value)
            except ObjectDoesNotExist:
                return value
            else:
                raise ValidationError('Team with the same name already exists.', code='team_already_exists')
        else:
            return value

    def create(self, validated_data):
        return Teams.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.team_name = validated_data.get('team_name', instance.full_name)
        instance.team_head_full_name = validated_data.get('team_head_full_name', instance.full_name)
        instance.team_head_email = validated_data.get('team_head_email', instance.full_name)
        instance.open_tickets = validated_data.get('open_tickets', instance.full_name)
        instance.closed_tickets_month = validated_data.get('closed_tickets_month', instance.full_name)
        instance.number_of_members = validated_data.get('number_of_members', instance.full_name)
        instance.save()
