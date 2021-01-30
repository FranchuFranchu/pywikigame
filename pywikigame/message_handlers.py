from .models import Match, Player
from django.core import serializers

websockets = []

__all__ = [ 
    "join_match",
    "create_match",
    "set_name",
    "set_ready",
    "match_list",
    "leave_match",
    "send_player_data",
    "log_page",
]

uid_requests = {}

def to_all_players(match, msg):
    print(uid_requests)
    for i in match.players.all():
        uid_requests[i.cookie].websocket.send(msg)

def create_match(request, **kwargs):
    match = Match.objects.create(**kwargs)
    request.websocket.send("success_create_match "+ serializers.serialize('json', [match]))

def join_match(request, pk, name):
    match = Match.objects.filter(pk=pk).first()
    player = Player.objects.filter(cookie=request.COOKIES["uid"]).first()
    if not player:
      player = Player.objects.create(cookie=request.COOKIES["uid"], match=match, name=name, page_log="")
    player.match = match
    to_all_players(player.match, f"add_player {serializers.serialize('json', [player])}")
    uid_requests[request.COOKIES["uid"]] = request

    request.websocket.send(f"this_player {serializers.serialize('json', [player])}")
    request.websocket.send(f"this_match {serializers.serialize('json', [match])}")

    for old_player in filter(lambda i: i is not player, player.match.players.all()):
        request.websocket.send(f"add_player {serializers.serialize('json', [old_player])}")

def set_name(request, name):
    player = Player.objects.filter(cookie=request.COOKIES["uid"])
    player.name = name
    player.save()
    
def set_ready(request, ready):
    player = Player.objects.filter(cookie=request.COOKIES["uid"]).first()
    player.ready = ready
    player.save()
    if player.match.check_start():
        to_all_players(player.match, 
            f"this_match {serializers.serialize('json', [player.match])}" )
    to_all_players(player.match, 
        f"add_player {serializers.serialize('json', [player])}" )

def log_page(request, page):
    e = Player.objects.filter(cookie=request.COOKIES["uid"]).first()
    e.page_log += " " + page
    print("log", Player.objects.filter(cookie=request.COOKIES["uid"]))
    to_all_players(e.match, f"add_player {serializers.serialize('json', [e])}")

def match_list(request):
    s = serializers.serialize('json', list(Match.objects.all()))
    request.websocket.send(f'match_list {s}')

def leave_match(request):
    player = Player.objects.filter(cookie=request.COOKIES["uid"]).first()
    if player:
        match = player.match
        to_all_players(match, f"delete_player {serializers.serialize('json', [player])}")
        player.delete()
        if not match.players.count():
            for ws in websockets:
                ws.websocket.send(f"delete_match {serializers.serialize('json', [match])}")
            match.delete()

def send_player_data(request):
    player = Player.objects.filter(cookie=request.COOKIES["uid"]).first()
    uid_requests[request.COOKIES["uid"]] = request
    if player:
        match = player.match
        request.websocket.send(f"this_player {serializers.serialize('json', [player])}")
        request.websocket.send(f"this_match {serializers.serialize('json', [match])}")
        for i in match.players.all():
            request.websocket.send(f"add_player {serializers.serialize('json', [i])}")

    request.websocket.send(f'not_logged_in {{}}')        