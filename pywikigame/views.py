from django.http import HttpResponse
from .wsfix import accept_websocket
from json import load, loads, dumps
from .message_handlers import websockets
import pywikigame.message_handlers as message_handlers

from traceback import format_exc

@accept_websocket
def websocket(request):
    if not request.is_websocket():
        return HttpResponse(code=400)
    else:
        websockets.append(request)
        message_handlers.send_player_data(request)
        for message in request.websocket:
            if message is None:
                continue
            print(message.decode('utf-8'))
            code, args = message.decode('utf-8').split(' ', 1)
            if code in message_handlers.__all__:
                try:
                    message_handlers.__dict__[code](request, **loads(args))
                except Exception as e:
                    request.websocket.send("error " + dumps(format_exc()))

            


def main_page(request):
    with open("static/index.html") as f:
        main_page_data = f.read()
    return HttpResponse(main_page_data)