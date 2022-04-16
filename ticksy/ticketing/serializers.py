from rest_framework import serializers
from .models import Employees,Teams


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
class EmployeesSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=50)
    department = serializers.CharField(max_length=50)
    team = serializers.CharField()

    def find_team_id(self):
        """
        Search in the database for the team
        """

    def create(self, validated_data):
        return Employees.objents.create(**validated_data)

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('fullname', instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.department = validated_data.get('department', instance.department)
        instance.team = validated_data.get('team',instance.team)
        instance.save()


    def set_team(self, instance, team_id):
        """
        Set the instance team to a valid team id, it's needed because the form will give the team name not id.
        """
        instance.team = team_id
        instance.save()

