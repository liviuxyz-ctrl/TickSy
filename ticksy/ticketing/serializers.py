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
        instance.password = validated_data.get('password', instance.password)
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


class TeamSerializer(serializers.Serializer):
    team_name = serializers.CharField(max_length=250)
    team_head_name = serializers.CharField(max_length=50)
    team_head_email = serializers.EmailField(max_length=50)

    # class Meta:
    #     model = Teams
    #     fields = ['team_name','team_head_full_name', 'team_head_email']

# team_name = models.CharField(max_length=250)
#     team_head_full_name = models.CharField(max_length=50)
#     team_head_email
