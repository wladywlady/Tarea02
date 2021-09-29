from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hello.serializers import PlayerSerializer
from hello.models import Player

from hello.serializers import LeagueSerializer
from hello.models import League

from hello.serializers import TeamSerializer
from hello.models import Team

from base64 import b64encode
path = "https://intense-brushlands-72593.herokuapp.com/"


from .models import Greeting


@api_view(['GET', 'POST'])
def league_list(request, **kwargs):
    """
    List all code snippets, or create a new snippet.
    """
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
        #dicc["_self"] = path +  "leagues/" + id_f[0:22]
        dicc["self"] = path +  "leagues/" + id_f[0:22]
        serializer = LeagueSerializer(data=dicc)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def league_detail(request, team_id, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        player = Player.objects.get(pk=pk)
    except Player.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlayerSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PlayerSerializer(player, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

@api_view(['GET', 'POST'])
def player_list(request, **kwargs):
 # serializer_class = BeaconSerializer
  #queryset = ''def list(self, request):
    if request.method == 'GET':
        players = Player.objects.all()
        all = []
        for player in players:
            dicc = {}
            dicc["id"] = player.id
            dicc["team_id"] = player.team_id
            dicc["name"] = player.name
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
        new_player = Player()
        string = info['name'] + info['position']
        id_f = b64encode(string.encode()).decode('utf-8')
        new_player.id = id_f[0:22]
        new_player.times_trained = 0
        liga = League.objects.get(id = kwargs.get('team_id'))
        #new_player.team_fkey =
        new_player.league = path +  "league/" + leagueid
        new_player.team = path +  "teams/" + data['team_id']
        new_player.self = path +  "players/" + data['id']

        #serializer = PlayerSerializer(data=request.data)
        serializer = PlayerSerializer(new_player)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def player_detail(request, team_id, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        player = Player.objects.get(pk=pk)
    except Player.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlayerSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PlayerSerializer(player, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





@api_view(['GET', 'POST'])
def team_list(request, **kwargs):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        info = request.data
        params = kwargs
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


    elif request.method == 'POST':
        info = request.data
        params = kwargs
        string = info['name'] + info['sport']
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
                dicc["self"] = league.self
                return Response(dicc,status=status.HTTP_409_CONFLICT)
        info['id'] =  id_f[0:22]
        info['teams'] = path +  "leagues/" + id_f[0:22]+  "/teams"
        info['players'] = path +  "leagues/" + id_f[0:22] +  "/players"
        info['self'] = path +  "leagues/" + id_f[0:22]
        serializer = LeagueSerializer(data=info)
        if serializer.is_valid():
            new_league.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def team_detail(request, team_id, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TeamSerializer(team)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TeamSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
