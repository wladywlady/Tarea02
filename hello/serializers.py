from rest_framework import serializers
from .models import Player
from .models import League
from .models import Team

from base64 import b64encode

path = "https://stark-stream-20032.herokuapp.com/"
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id','team_id','name', 'age', 'position','self')

PlayerSerializer._declared_fields["self"] = serializers.CharField(source="_self")

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ['id','name','sport','teams','players','self']

LeagueSerializer._declared_fields["self"] = serializers.CharField(source="_self")

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id','league_id','name','city','league','players','self')

TeamSerializer._declared_fields["self"] = serializers.CharField(source="_self")
