from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

class League(models.Model):
    league_id = models.AutoField(primary_key=True)
    id = models.CharField(max_length = 100,blank=True)
    #id = models.CharField(primary_key=True, max_length = 100)
    name = models.CharField(max_length = 100)
    sport = models.CharField(max_length = 100)
    league = models.CharField(max_length = 100,blank=True)
    teams = models.CharField(max_length = 100,blank=True)
    self = models.CharField(max_length = 100,blank=True)

    def __str__(self):
        return self.headline

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    id = models.TextField(blank=True)
    #id = models.CharField(primary_key=True, max_length = 100)
    league_id = models.CharField(max_length = 100,blank=True)
    name = models.CharField(max_length = 100)
    city = models.CharField(max_length = 100)
    #league_fkey = models.ForeignKey(League, on_delete=models.CASCADE)
    league = models.CharField(max_length = 100,blank=True)
    players = models.CharField(max_length = 100,blank=True)
    self = models.CharField(max_length = 100,blank=True)

    def __str__(self):
        return self.headline

class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    id = models.CharField(max_length = 100,blank=True)
    #id = models.CharField(primary_key=True, max_length = 100)
    team_id = models.CharField(max_length = 100,blank=True)
    name = models.CharField(max_length = 100)
    age = models.IntegerField()
    position = models.CharField(max_length = 100)
    times_trained = models.IntegerField(default = 0)
    #team_fkey = models.ForeignKey(Team, blank=True, on_delete=models.CASCADE)
    league = models.CharField(max_length = 100,blank=True)
    team = models.CharField(max_length = 100,blank=True)
    self = models.CharField(max_length = 100,blank=True)

    def __str__(self):
        return self.headline
