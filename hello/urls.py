from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from hello import views

urlpatterns = [


    path("leagues", views.league_list,name="league_list"),
    path("teams", views.team_list,name="team_list"),
    path("players", views.player_list,name="team_list"),


    path("leagues/<str:league_id>", views.league_detail,name="league_detail"),
    path("teams/<str:team_id>", views.team_detail,name="player_create"),
    path("players/<str:player_id>", views.player_detail,name="team_list"),


    path("teams/<str:team_id>/players", views.player_list,name="player_create"),
    path("leagues/<str:league_id>/teams", views.team_list,name="team_create"),



    path("leagues/<str:league_id>/teams/train:", views.league_train,name="league_detail"),
    path("players/<str:player_id>/train", views.player_train,name="league_detail"),
    path("teams/<str:team_id>/players/train", views.team_train,name="league_detail"),



]

urlpatterns = format_suffix_patterns(urlpatterns)
