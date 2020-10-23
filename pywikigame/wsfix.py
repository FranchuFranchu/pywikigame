from django.shortcuts import render
from dwebsocket.middleware import WebSocketMiddleware
from django.conf import settings
from django.http import HttpResponse
from django.utils.decorators import decorator_from_middleware

import logging
import importlib
from django.conf import settings
from django.http import HttpResponseBadRequest
from dwebsocket.factory import WebSocketFactory


WEBSOCKET_ACCEPT_ALL = getattr(settings, 'WEBSOCKET_ACCEPT_ALL', False)
WEBSOCKET_FACTORY_CLASS = getattr(
    settings,
    'WEBSOCKET_FACTORY_CLASS',
    'dwebsocket.backends.default.factory.WebSocketFactory',
)

logger = logging.getLogger(__name__)


class WebSocketMiddleware(object):
    def __init__(self, cls):
        pass

    @classmethod
    def process_request(cls, request):
        try:
            offset = WEBSOCKET_FACTORY_CLASS.rindex(".")
            
            factory_cls = getattr(
                importlib.import_module(WEBSOCKET_FACTORY_CLASS[:offset]),
                WEBSOCKET_FACTORY_CLASS[offset+1:]
            )
            request.websocket = factory_cls(request).create_websocket()
        except ValueError as e:
            logger.debug(e)
            request.websocket = None
            request.is_websocket = lambda: False
            return HttpResponseBadRequest()
        if request.websocket is None:
            request.is_websocket = lambda: False
        else:
            request.is_websocket = lambda: True

    @classmethod
    def process_view(cls, request, view_func, view_args, view_kwargs):
        # open websocket if its an accepted request
        if request.is_websocket():
            # deny websocket request if view can't handle websocket
            if not WEBSOCKET_ACCEPT_ALL and \
                not getattr(view_func, 'accept_websocket', False):
                return HttpResponseBadRequest()
            # everything is fine .. so prepare connection by sending handshake
            request.websocket.accept_connection()
        elif getattr(view_func, 'require_websocket', False):
            # websocket was required but not provided
            return HttpResponseBadRequest()

    @classmethod
    def process_response(cls, request, response):
        if request.is_websocket():
            request.websocket.close()
        return response

    @classmethod
    def process_exception(cls, request, exception):
        if request.is_websocket():
            request.websocket.close()


# Create your views here.


WEBSOCKET_MIDDLEWARE_INSTALLED = False

def _setup_websocket(func):
    from functools import wraps
    @wraps(func)
    def new_func(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        if response is None and request.is_websocket():
            response =  HttpResponse()
            response.__len__ = lambda : 0
            return response
        return response
    if not WEBSOCKET_MIDDLEWARE_INSTALLED:
        decorator = decorator_from_middleware(WebSocketMiddleware)
        new_func = decorator(new_func)
    return new_func


def accept_websocket(func):
    func.accept_websocket = True
    func.require_websocket = getattr(func, 'require_websocket', False)
    func = _setup_websocket(func)
    return func

