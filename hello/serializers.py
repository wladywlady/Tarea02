from rest_framework import serializers
from .models import Player
from .models import League
from base64 import b64encode

path = "https://ancient-badlands-43562.herokuapp.com/"
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id','team_id','name', 'age', 'position')

    def to_representation(self, data):
        data = super(PlayerSerializer, self).to_representation(data)
        string = data['name'] + ':' +data['position']
        id_f = b64encode(string.encode()).decode('utf-8')
        data['id'] = id_f[0:22]
        data['times_trained'] = 0
        data['league'] = path +  "league/"
        data['team'] = path +  "teams/"
        data['self'] = path +  "players/" + data['id']
        return data
#Si existe otro mismo ID no agregar

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ('id','name','sport')

    def to_representation(self, data):
        data = super(LeagueSerializer, self).to_representation(data)
        string = data['name'] + ':' + data['sport']
        id_f = b64encode(string.encode()).decode('utf-8')
        data['id'] = id_f[0:22]
        data['teams'] = path +  "teams/"
        data['players'] = path +  "players/"
        data['self'] = path +  "players/" + data['id']
        return data
#Si existe otro mismo ID no agregar
