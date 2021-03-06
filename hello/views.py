from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hello.serializers import PlayerSerializer
from hello.models import Player

from hello.serializers import LeagueSerializer
from .models import League

from hello.serializers import TeamSerializer
from hello.models import Team

from base64 import b64encode
path = "https://integracion-tarea02-wnvv.herokuapp.com/"


from .models import Greeting

#lIGAS
@api_view(['GET', 'POST'])
def league_list(request, **kwargs):

    if request.method == 'GET':
        leagues = League.objects.all()
        all = []
        for league in leagues:
            dicc = {}
            dicc["id"] = league.id
            dicc["name"] = league.name
            dicc["sport"] = league.sport
            dicc["teams"] = league.teams
            dicc["players"] = league.players
            dicc["self"] = league._self
            all.append(dicc)
        return Response(all, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        info = request.data
        params = kwargs
        try:
          info['name']
          info['sport']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        string = info['name'] + ':' + info['sport']
        id_f = b64encode(string.encode()).decode('utf-8')
        leagues = League.objects.all()
        for league in leagues:
            if league.id == id_f[0:22]:
                dicc = {}
                dicc["id"] = league.id
                dicc["name"] = league.name
                dicc["sport"] = league.sport
                dicc["teams"] = league.teams
                dicc["players"] = league.players
                dicc["self"] = league._self
                return Response(dicc,status=status.HTTP_409_CONFLICT)
        dicc  = {}
        dicc["id"] = id_f[0:22]
        dicc["name"] = info['name']
        dicc["sport"] = info['sport']
        dicc["teams"] = path +  "leagues/" + id_f[0:22]+  "/teams"
        dicc["players"] = path +  "leagues/" + id_f[0:22] +  "/players"
        dicc["self"] = path +  "leagues/" + id_f[0:22]
        serializer = LeagueSerializer(data=dicc)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def league_detail(request, league_id, format=None):
    if request.method == 'GET':
        try:
            league = League.objects.get(id=league_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        leagues = League.objects.all()
        dicc = {}
        for league in leagues:
            if league.id == league_id:
                dicc["id"] = league.id
                dicc["name"] = league.name
                dicc["sport"] = league.sport
                dicc["teams"] = league.teams
                dicc["players"] = league.players
                dicc["self"] = league._self
                return Response(dicc, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    elif request.method == 'DELETE':
        try:
            league = League.objects.get(id=league_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        league = League.objects.get(id=league_id)
        teams = Team.objects.all()
        for team in teams:
            if team.league_id == league_id:
                players = Team.objects.get(id=team.id)
                for player in players:
                    player.delete()
                team.delete()

        league.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def league_train(request, league_id, format=None):
    try:
        league = League.objects.get(id=league_id)
    except league.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    teams = Team.objects.all()
    for team in teams:
        players = Team.objects.get(id=team.id)
        for player in players:
            dicc = {}
            dicc["times_trained"] = player.times_trained + 1
            serializer = PlayerSerializer(player, data=dicc, partial=True)
            if serializer.is_valid():
                serializer.save()

    return Response(status=status.HTTP_200_OK)


#TEAMS
@api_view(['GET', 'POST'])
def team_list(request, **kwargs):

    if request.method == 'GET':
        teams = Team.objects.all()
        all = []
        for team in teams:
            dicc = {}
            dicc["id"] = team.id
            dicc["league_id"] = team.league_id
            dicc["name"] = team.name
            dicc["city"] = team.city
            dicc["league"] = team.league
            dicc["players"] = team.players
            dicc["self"] = team._self
            all.append(dicc)
        return Response(all, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        info = request.data
        params = kwargs
        try:
          info['name']
          info['city']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            league = League.objects.get(id=params["league_id"])
        except:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)



        string = info['name'] + ':' + info['city']
        id_f = b64encode(string.encode()).decode('utf-8')
        teams = Team.objects.all()
        for team in teams:
            if team.id == id_f[0:22]:
                dicc = {}
                dicc["id"] = team.id
                dicc["league_id"] = team.league_id
                dicc["name"] = team.name
                dicc["city"] = team.city
                dicc["league"] = team.league
                dicc["players"] = team.players
                dicc["self"] = team._self
                return Response(dicc,status=status.HTTP_409_CONFLICT)
        dicc  = {}
        dicc["id"] = id_f[0:22]
        dicc["league_id"] = params["league_id"]
        dicc["name"] = info['name']
        dicc["city"] = info['city']
        dicc["league"] =  path +  "leagues/" + params["league_id"]
        dicc["players"] = path +  "teams/" + id_f[0:22] +  "/players"
        dicc["self"] = path +  "teams/" + id_f[0:22]
        serializer = TeamSerializer(data=dicc)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def team_detail(request, team_id, format=None):

    if request.method == 'GET':
        try:
            team = Team.objects.get(id=team_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        teams = Team.objects.all()
        dicc = {}
        for team in teams:
            if team.id == team_id:
                dicc["id"] = team.id
                dicc["league_id"] = team.league_id
                dicc["name"] = team.name
                dicc["city"] = team.city
                dicc["league"] = team.league
                dicc["players"] = team.players
                dicc["self"] = team._self
                return Response(dicc, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    elif request.method == 'DELETE':
        try:
            team = Team.objects.get(id=team_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        team = Team.objects.get(id=team_id)
        players = Player.objects.all()
        for player in players:
            if player.team_id == team_id:
                player.delete()
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def team_train(request, team_id, format=None):
    try:
        team = Team.objects.get(id=team_id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


    players = Player.objects.all()
    for player in players:
        dicc = {}
        dicc["times_trained"] = player.times_trained + 1
        serializer = PlayerSerializer(player, data=dicc, partial=True)
        if serializer.is_valid():
            serializer.save()

    return Response(status=status.HTTP_200_OK)


#PLAYERS
@api_view(['GET', 'POST'])
def player_list(request, **kwargs):

    if request.method == 'GET':
        all = []
        players = Player.objects.all()
        for player in players:
            dicc = {}
            dicc["id"] = player.id
            dicc["team_id"] = player.team_id
            dicc["name"] = player.name
            dicc["age"] = player.age
            dicc["position"] = player.position
            dicc["times_trained"] = player.times_trained
            dicc["league"] = player.league
            dicc["team"] = player.team
            dicc["self"] = player._self
            all.append(dicc)
        return Response(all, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        info = request.data
        params = kwargs
        try:
          info['name']
          info['age']
          info['position']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            team = Team.objects.get(id=params["team_id"])
        except:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        string = info['name'] + ':' + info['position']
        id_f = b64encode(string.encode()).decode('utf-8')
        players = Player.objects.all()
        for player in players:
            if player.id == id_f[0:22]:
                dicc = {}
                dicc["id"] = player.id
                dicc["team_id"] = player.team_id
                dicc["name"] = player.name
                dicc["age"] = player.age
                dicc["position"] = player.position
                dicc["times_trained"] = player.times_trained
                dicc["league"] = player.league
                dicc["team"] = player.team
                dicc["self"] = player._self
                return Response(dicc,status=status.HTTP_409_CONFLICT)
        try:
            team = Team.objects.get(id=params["team_id"])
            league = League.objects.get(id=team.league_id)
        except:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        team = Team.objects.get(id=params["team_id"])
        league = League.objects.get(id=team.league_id)

        dicc  = {}
        dicc["id"] = id_f[0:22]
        dicc["team_id"] = params["team_id"]
        dicc["name"] = info['name']
        dicc["age"] = info['age']
        dicc["position"] = info['position']
        dicc["times_trained"] = 0
        dicc["league"] = path +  "leagues/" + team.league_id
        dicc["team"] = path +  "teams/" + params["team_id"]
        dicc["self"] = path +  "players/" + id_f[0:22]
        serializer = PlayerSerializer(data=dicc)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'POST':
        info = request.data
        params = kwargs
        try:
          info['name']
          info['position']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


        string = info['name'] + info['position']
        id_f = b64encode(string.encode()).decode('utf-8')
        players = Player.objects.all()
        for player in players:
            if player.id == id_f[0:22]:
                dicc = {}
                dicc["id"] = league.id
                dicc["team_id"] = league.name
                dicc["name"] = league.name
                dicc["sport"] = league.sport
                dicc["age"] = league.sport
                dicc["position"] = league.teams
                dicc["times_trained"] = league.teams
                dicc["league"] = league.players
                dicc["team"] = league.players
                dicc["self"] = league._self
                return Response(dicc,status=status.HTTP_409_CONFLICT)

        new_player = Player()

        new_player.id = id_f[0:22]
        new_player.times_trained = 0

        #serializer = PlayerSerializer(data=request.data)
        serializer = PlayerSerializer(new_player)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def player_detail(request, player_id, format=None):

    if request.method == 'GET':
        try:
            player = Player.objects.get(id=player_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        players = Player.objects.all()
        dicc = {}
        for player in players:
            if player.id == player_id:
                dicc["id"] = player.id
                dicc["team_id"] = player.team_id
                dicc["name"] = player.name
                dicc["age"] = player.age
                dicc["position"] = player.position
                dicc["times_trained"] = player.times_trained
                dicc["league"] = player.league
                dicc["team"] = player.team
                dicc["self"] = player._self
                return Response(dicc, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    elif request.method == 'DELETE':
        try:
            player = Player.objects.get(id=player_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        player = Player.objects.get(id=player_id)
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def player_train(request, player_id, format=None):
    try:
        player = Player.objects.get(id=player_id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    player = Player.objects.get(id=player_id)
    dicc["times_trained"] = player.times_trained + 1
    serializer = PlayerSerializer(player, data=dicc, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(status=status.HTTP_200_OK)





def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")

def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, "db.html", {"greetings": greetings})
