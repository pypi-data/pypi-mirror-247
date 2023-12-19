# Klipper Web Server Rest API
#
# Copyright (C) 2020 Eric Callahan <arksine.code@gmail.com>
#
# This file may be distributed under the terms of the GNU GPLv3 license

from __future__ import annotations
import os
import mimetypes
import logging
import json
import traceback
import ssl
import urllib.parse
import io
import tornado
import tornado.iostream
import tornado.httputil
import tornado.web
from inspect import isclass
from tornado.escape import url_unescape
from tornado.routing import Rule, PathMatches, AnyMatches
from tornado.http1connection import HTTP1Connection
from tornado.log import access_log
from PIL import Image

from stereotech_cloud_commons.components.mongo_database import parse_json
from .utils import ServerError
from .websockets import WebRequest, WebsocketManager, WebSocket

# Annotation imports
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
    Callable,
    Coroutine,
    Union,
    Dict,
    List,
    AsyncGenerator,
)
if TYPE_CHECKING:
    from tornado.httpserver import HTTPServer
    from .stereotech_cloud import Server
    from .eventloop import EventLoop
    from .confighelper import ConfigHelper
    from .websockets import APITransport, NotificationTransport
    from .components import authorization
    MessageDelgate = Optional[tornado.httputil.HTTPMessageDelegate]
    AuthComp = Optional[authorization.Authorization]
    APICallback = Callable[[WebRequest], Coroutine]

# 50 MiB Max Standard Body Size
MAX_BODY_SIZE = 50 * 1024 * 1024
EXCLUDED_ARGS = ["_", "token", "access_token", "connection_id"]
AUTHORIZED_EXTS = [".png"]
ALL_TRANSPORTS = ["http", "websocket", "mqtt", "cloud"]


class MutableRouter(tornado.web.ReversibleRuleRouter):
    def __init__(self, application: StereotechCloud) -> None:
        self.application = application
        self.pattern_to_rule: Dict[str, Rule] = {}
        super(MutableRouter, self).__init__(None)

    def get_target_delegate(self,
                            target: Any,
                            request: tornado.httputil.HTTPServerRequest,
                            **target_params
                            ) -> MessageDelgate:
        if isclass(target) and issubclass(target, tornado.web.RequestHandler):
            return self.application.get_handler_delegate(
                request, target, **target_params)

        return super(MutableRouter, self).get_target_delegate(
            target, request, **target_params)

    def has_rule(self, pattern: str) -> bool:
        return pattern in self.pattern_to_rule

    def add_handler(self,
                    pattern: str,
                    target: Any,
                    target_params: Optional[Dict[str, Any]]
                    ) -> None:
        if pattern in self.pattern_to_rule:
            self.remove_handler(pattern)
        new_rule = Rule(PathMatches(pattern), target, target_params)
        self.pattern_to_rule[pattern] = new_rule
        self.rules.append(new_rule)

    def remove_handler(self, pattern: str) -> None:
        rule = self.pattern_to_rule.pop(pattern, None)
        if rule is not None:
            try:
                self.rules.remove(rule)
            except Exception:
                logging.exception(f"Unable to remove rule: {pattern}")


class APIDefinition:
    def __init__(self,
                 endpoint: str,
                 http_uri: str,
                 jrpc_methods: List[str],
                 request_methods: Union[str, List[str]],
                 transports: List[str],
                 callback: APICallback,
                 need_object_parser: bool,
                 scopes: Dict[str, List[str]] = {
                     "get": [], "post": [], "delete": []},
                 ):
        self.endpoint = endpoint
        self.uri = http_uri
        self.jrpc_methods = jrpc_methods
        if not isinstance(request_methods, list):
            request_methods = [request_methods]
        self.request_methods = request_methods
        self.supported_transports = transports
        self.callback = callback
        self.need_object_parser = need_object_parser
        self.scopes = scopes


class NotificationDefinition:
    def __init__(self, evt_name: str, notify_name: Optional[str] = None, transports: List[str] = ['websocket', 'mq']):
        self.event_name = evt_name
        self.notify_name = notify_name
        self.supported_transports = transports


class StereotechCloud:
    def __init__(self, config: ConfigHelper) -> None:
        self.server = config.get_server()
        self.http_server: Optional[HTTPServer] = None
        self.secure_server: Optional[HTTPServer] = None
        self.api_cache: Dict[str, APIDefinition] = {}
        self.notification_cache: Dict[str, NotificationDefinition] = {}
        self.registered_base_handlers: List[str] = []
        self.max_upload_size = config.getint('max_upload_size', 1024)
        self.max_upload_size *= 1024 * 1024

        # SSL config
        self.cert_path: str = self._get_path_option(
            config, 'ssl_certificate_path')
        self.key_path: str = self._get_path_option(
            config, 'ssl_key_path')

        # Set Up Websocket and Authorization Managers
        self.wsm = WebsocketManager(self.server)
        self.api_transports: Dict[str, APITransport] = {
            "websocket": self.wsm
        }

        self.notification_transports: Dict[str, NotificationTransport] = {
            "websocket": self.wsm
        }

        self.middlewares: List[Callable[[WebRequest], Coroutine]] = []
        mimetypes.add_type('text/plain', '.log')
        mimetypes.add_type('text/plain', '.gcode')
        mimetypes.add_type('text/plain', '.cfg')

        self.debug = config.getboolean('enable_debug_logging', False)
        log_level = logging.DEBUG if self.debug else logging.INFO
        logging.getLogger().setLevel(log_level)
        app_args: Dict[str, Any] = {
            'serve_traceback': self.debug,
            'websocket_ping_interval': 10,
            'websocket_ping_timeout': 30,
            'parent': self,
            'default_handler_class': AuthorizedErrorHandler,
            'default_handler_args': {},
            'log_function': self.log_request
        }

        # Set up HTTP only requests
        self.mutable_router = MutableRouter(self)
        app_handlers: List[Any] = [
            (AnyMatches(), self.mutable_router),
            (r"/websocket", WebSocket),
            (r"/server/redirect", RedirectHandler)]
        self.app = tornado.web.Application(app_handlers, **app_args)
        self.get_handler_delegate = self.app.get_handler_delegate

        # Register handlers
        logfile = self.server.get_app_args().get('log_file')
        if logfile:
            self.register_static_file_handler(
                "stereotech_cloud.log", logfile, force=True)

    def _get_path_option(self, config: ConfigHelper, option: str) -> str:
        path: Optional[str] = config.get(option, None)
        if path is None:
            return ""
        expanded = os.path.abspath(os.path.expanduser(path))
        if not os.path.exists(expanded):
            raise self.server.error(
                f"Invalid path for option '{option}', "
                f"{path} does not exist")
        return expanded

    def listen(self, host: str, port: int, ssl_port: int) -> None:
        self.http_server = self.app.listen(
            port, address=host, max_body_size=MAX_BODY_SIZE,
            xheaders=True)
        if os.path.exists(self.cert_path) and os.path.exists(self.key_path):
            logging.info(f"Starting secure server on port {ssl_port}")
            ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_ctx.load_cert_chain(self.cert_path, self.key_path)
            self.secure_server = self.app.listen(
                ssl_port, address=host, max_body_size=MAX_BODY_SIZE,
                xheaders=True, ssl_options=ssl_ctx)
        else:
            logging.info("SSL Certificate/Key not configured, "
                         "aborting HTTPS Server startup")

    def log_request(self, handler: tornado.web.RequestHandler) -> None:
        status_code = handler.get_status()
        if not self.debug and status_code in [200, 204, 206, 304]:
            # don't log successful requests in release mode
            return
        if status_code < 400:
            log_method = access_log.info
        elif status_code < 500:
            log_method = access_log.warning
        else:
            log_method = access_log.error
        request_time = 1000.0 * handler.request.request_time()
        user = handler.current_user
        username = "No User"
        if user is not None and 'username' in user:
            username = user['username']
        log_method(
            f"{status_code} {handler._request_summary()} "
            f"[{username}] {request_time:.2f}ms")

    def get_server(self) -> Server:
        return self.server

    def get_websocket_manager(self) -> WebsocketManager:
        return self.wsm

    async def close(self) -> None:
        if self.http_server is not None:
            self.http_server.stop()
            await self.http_server.close_all_connections()
        if self.secure_server is not None:
            self.secure_server.stop()
            await self.secure_server.close_all_connections()
        await self.wsm.close()

    def register_api_transport(self,
                               name: str,
                               transport: APITransport
                               ) -> Dict[str, APIDefinition]:
        self.api_transports[name] = transport
        return self.api_cache

    def register_notification_transport(self,
                                        name: str,
                                        transport: NotificationTransport) -> Dict[str, NotificationDefinition]:
        self.notification_transports[name] = transport
        return self.notification_cache

    def register_notification(self,
                              event_name: str,
                              notify_name: Optional[str] = None,
                              transports: List[str] = ['websocket', 'mq']
                              ) -> None:
        self.notification_cache[event_name] = NotificationDefinition(
            event_name, notify_name, transports)
        for name, transport in self.notification_transports.items():
            if name in transports:
                transport.register_notification(event_name, notify_name)

    def register_local_handler(self,
                               uri: str,
                               request_methods: List[str],
                               callback: APICallback,
                               transports: List[str] = ALL_TRANSPORTS,
                               wrap_result: bool = True,
                               scopes: Dict[str, List[str]] = {
                                   "get": [], "post": [], "delete": []},
                               ) -> None:
        if uri in self.registered_base_handlers:
            return
        api_def = self._create_api_definition(
            uri, callback, request_methods, transports=transports)
        if "http" in transports:
            logging.info(
                f"Registering HTTP Endpoint: "
                f"({' '.join(request_methods)}) {uri}")
            params: dict[str, Any] = {}
            params['methods'] = request_methods
            params['callback'] = callback
            params['wrap_result'] = wrap_result
            params['is_remote'] = False
            params['scopes'] = scopes
            params['middlewares'] = self.middlewares
            self.mutable_router.add_handler(uri, DynamicRequestHandler, params)
        self.registered_base_handlers.append(uri)
        for name, transport in self.api_transports.items():
            if name in transports:
                transport.register_api_handler(api_def)

    def register_middleware(self, callback: Callable[[WebRequest], Coroutine[WebRequest]], index: Optional[int] = None):
        if index is not None:
            self.middlewares.insert(index, callback)
        else:
            self.middlewares.append(callback)

    def register_static_file_handler(self,
                                     pattern: str,
                                     file_path: str,
                                     force: bool = False,
                                     ) -> None:
        if pattern[0] != "/":
            pattern = "/server/files/" + pattern
        if os.path.isfile(file_path) or force:
            pattern += '()'
        elif os.path.isdir(file_path):
            if pattern[-1] != "/":
                pattern += "/"
            pattern += "(.*)"
        else:
            logging.info(f"Invalid file path: {file_path}")
            return
        logging.debug(f"Registering static file: ({pattern}) {file_path}")
        params = {"path": file_path}
        self.mutable_router.add_handler(pattern, CustomFileHandler, params)

    def remove_handler(self, endpoint: str) -> None:
        api_def = self.api_cache.pop(endpoint, None)
        if api_def is not None:
            self.mutable_router.remove_handler(api_def.uri)
            for name, transport in self.api_transports.items():
                transport.remove_api_handler(api_def)

    def _create_api_definition(self,
                               endpoint: str,
                               callback: APICallback,
                               request_methods: List[str] = [],

                               transports: List[str] = ALL_TRANSPORTS
                               ) -> APIDefinition:
        if endpoint in self.api_cache:
            return self.api_cache[endpoint]
        if endpoint[0] == '/':
            uri = endpoint
        else:
            uri = "/server/" + endpoint
        jrpc_methods = []
        name_parts = uri[1:].split('/')
        if len(request_methods) > 1:
            for req_mthd in request_methods:
                func_name = req_mthd.lower() + "_" + name_parts[-1]
                jrpc_methods.append(".".join(
                    name_parts[:-1] + [func_name]))
        else:
            jrpc_methods.append(".".join(name_parts))
        if len(request_methods) != len(jrpc_methods):
            raise self.server.error(
                "Invalid API definition.  Number of websocket methods must "
                "match the number of request methods")
        need_object_parser = endpoint.startswith("objects/")
        api_def = APIDefinition(endpoint, uri, jrpc_methods, request_methods,
                                transports, callback, need_object_parser)
        self.api_cache[endpoint] = api_def
        return api_def


class AuthorizedRequestHandler(tornado.web.RequestHandler):
    def initialize(self) -> None:
        self.server: Server = self.settings['parent'].get_server()

    def set_default_headers(self) -> None:
        origin: Optional[str] = self.request.headers.get("Origin")
        # it is necessary to look up the parent app here,
        # as initialize() may not yet be called
        server: Server = self.settings['parent'].get_server()
        auth: AuthComp = server.lookup_component('authorization', None)
        self.cors_enabled = False
        if auth is not None:
            self.cors_enabled = auth.check_cors(origin, self)

    async def prepare(self) -> None:
        auth: AuthComp = self.server.lookup_component('authorization', None)
        if auth is None:
            auth = self.server.lookup_component(
                'external_authorization', None)
        if auth is not None:
            self.current_user = await auth.check_authorized(self.request)

    def options(self, *args, **kwargs) -> None:
        # Enable CORS if configured
        if self.cors_enabled:
            self.set_status(204)
            self.finish()
        else:
            super(AuthorizedRequestHandler, self).options()

    def get_associated_websocket(self) -> Optional[WebSocket]:
        # Return associated websocket connection if an id
        # was provided by the request
        conn = None
        conn_id: Any = self.get_argument('connection_id', None)
        if conn_id is not None:
            try:
                conn_id = int(conn_id)
            except Exception:
                pass
            else:
                parent: StereotechCloud = self.settings['parent']
                wsm: WebsocketManager = parent.get_websocket_manager()
                conn = wsm.get_websocket(conn_id)
        return conn

    def write_error(self, status_code: int, **kwargs) -> None:
        err = {'code': status_code, 'message': self._reason}
        if 'exc_info' in kwargs:
            err['traceback'] = "\n".join(
                traceback.format_exception(*kwargs['exc_info']))
        self.finish({'error': err})

# Due to the way Python treats multiple inheritance its best
# to create a separate authorized handler for serving files


class AuthorizedFileHandler(tornado.web.StaticFileHandler):
    def initialize(self,
                   path: str,
                   default_filename: Optional[str] = None
                   ) -> None:
        super(AuthorizedFileHandler, self).initialize(path, default_filename)
        self.server: Server = self.settings['parent'].get_server()

    def set_default_headers(self) -> None:
        origin: Optional[str] = self.request.headers.get("Origin")
        # it is necessary to look up the parent app here,
        # as initialize() may not yet be called
        server: Server = self.settings['parent'].get_server()
        auth: AuthComp = server.lookup_component('authorization', None)
        self.cors_enabled = False
        if auth is not None:
            self.cors_enabled = auth.check_cors(origin, self)

    async def prepare(self) -> None:
        auth: AuthComp = self.server.lookup_component('authorization', None)
        if auth is None:
            auth = self.server.lookup_component(
                'external_authorization', None)
        if auth is not None and self._check_need_auth():
            self.current_user = await auth.check_authorized(self.request)

    def options(self, *args, **kwargs) -> None:
        # Enable CORS if configured
        if self.cors_enabled:
            self.set_status(204)
            self.finish()
        else:
            super(AuthorizedFileHandler, self).options()

    def write_error(self, status_code: int, **kwargs) -> None:
        err = {'code': status_code, 'message': self._reason}
        if 'exc_info' in kwargs:
            err['traceback'] = "\n".join(
                traceback.format_exception(*kwargs['exc_info']))
        self.finish({'error': err})

    def _check_need_auth(self) -> bool:
        if self.request.method != "GET":
            return True
        ext = os.path.splitext(self.request.path)[-1].lower()
        if ext in AUTHORIZED_EXTS:
            return False
        return True


class DynamicRequestHandler(AuthorizedRequestHandler):
    def initialize(
        self,
        callback: Union[str, Callable[[WebRequest], Coroutine]] = "",
        methods: List[str] = [],
        need_object_parser: bool = False,
        is_remote: bool = True,
        wrap_result: bool = True,
        scopes: Dict[str, List[str]] = {"get": [], "post": [], "delete": []},
        middlewares: List[Callable[[WebRequest], Coroutine]] = []
    ) -> None:
        super(DynamicRequestHandler, self).initialize()
        self.callback = callback
        self.methods = methods
        self.wrap_result = wrap_result
        self.scopes = scopes
        self.middlewares = middlewares
        self._do_request = self._do_local_request
        self._parse_query = self._object_parser if need_object_parser \
            else self._default_parser

    # Converts query string values with type hints
    def _convert_type(self, value: str, hint: str) -> Any:
        type_funcs: Dict[str, Callable] = {
            "int": int, "float": float,
            "bool": lambda x: x.lower() == "true",
            "json": json.loads}
        if hint not in type_funcs:
            logging.info(f"No conversion method for type hint {hint}")
            return value
        func = type_funcs[hint]
        try:
            converted = func(value)
        except Exception:
            logging.exception("Argument conversion error: Hint: "
                              f"{hint}, Arg: {value}")
            return value
        return converted

    def _default_parser(self) -> Dict[str, Any]:
        args = {}
        for key in self.request.arguments.keys():
            if key in EXCLUDED_ARGS:
                continue
            key_parts = key.rsplit(":", 1)
            val = self.get_argument(key)
            if len(key_parts) == 1:
                args[key] = val
            else:
                args[key_parts[0]] = self._convert_type(val, key_parts[1])
        return args

    def _object_parser(self) -> Dict[str, Dict[str, Any]]:
        args: Dict[str, Any] = {}
        for key in self.request.arguments.keys():
            if key in EXCLUDED_ARGS:
                continue
            val = self.get_argument(key)
            if not val:
                args[key] = None
            else:
                args[key] = val.split(',')
        logging.debug(f"Parsed Arguments: {args}")
        return {'objects': args}

    def parse_args(self) -> Dict[str, Any]:
        try:
            args = self._parse_query()
        except Exception:
            raise ServerError(
                "Error Parsing Request Arguments. "
                "Is the Content-Type correct?")
        content_type = self.request.headers.get('Content-Type', "").strip()
        if content_type.startswith("application/json"):
            try:
                args.update(json.loads(self.request.body))
            except json.JSONDecodeError:
                pass
        for key, value in self.path_kwargs.items():
            if value is not None:
                args[key] = value
        return args

    async def get(self, *args, **kwargs) -> None:
        await self._process_http_request()

    async def post(self, *args, **kwargs) -> None:
        await self._process_http_request()

    async def delete(self, *args, **kwargs) -> None:
        await self._process_http_request()

    async def _do_local_request(self,
                                args: Dict[str, Any],
                                conn: Optional[WebSocket]
                                ) -> Any:
        assert callable(self.callback)
        wr = WebRequest(self.request.path, args, action=self.request.method,
                        headers=self.request.headers, conn=conn,
                        ip_addr=self.request.remote_ip, user=self.current_user,
                        scopes=self.scopes)
        for middleware in self.middlewares:
            wr = await middleware(wr)
        return await self.callback(wr)

    async def _process_http_request(self) -> None:
        if self.request.method not in self.methods:
            raise tornado.web.HTTPError(405)
        conn = self.get_associated_websocket()
        args = self.parse_args()
        try:
            result = await self._do_request(args, conn)
            result = parse_json(result)
        except ServerError as e:
            raise tornado.web.HTTPError(
                e.status_code, str(e)) from e
        if self.wrap_result:
            result = {'result': result}
        self.finish(result)


class FileRequestHandler(AuthorizedFileHandler):
    def set_extra_headers(self, path: str) -> None:
        # The call below shold never return an empty string,
        # as the path should have already been validated to be
        # a file
        assert isinstance(self.absolute_path, str)
        basename = os.path.basename(self.absolute_path)
        ascii_basename = self._escape_filename_to_ascii(basename)
        utf8_basename = self._escape_filename_to_utf8(basename)
        self.set_header(
            "Content-Disposition", f"attachment; filename={ascii_basename}; "
                                   f"filename*=UTF-8\'\'{utf8_basename}")

    async def delete(self, path: str) -> None:
        raise tornado.web.HTTPError(
            403, "File is loaded, DELETE not permitted")

    async def get(self, path: str, include_body: bool = True) -> None:
        # Set up our path instance variables.
        self.path = self.parse_url_path(path)
        del path  # make sure we don't refer to path instead of self.path again
        absolute_path = self.get_absolute_path(self.root, self.path)
        self.absolute_path = self.validate_absolute_path(
            self.root, absolute_path)
        if self.absolute_path is None:
            return

        self.modified = self.get_modified_time()
        self.set_headers()

        self.request.headers.pop("If-None-Match", None)
        if self.should_return_304():
            self.set_status(304)
            return

        request_range = None
        range_header = self.request.headers.get("Range")
        if range_header:
            # As per RFC 2616 14.16, if an invalid Range header is specified,
            # the request will be treated as if the header didn't exist.
            request_range = tornado.httputil._parse_request_range(range_header)

        size = self.get_content_size()
        if request_range:
            start, end = request_range
            if start is not None and start < 0:
                start += size
                if start < 0:
                    start = 0
            if (
                start is not None
                and (start >= size or (end is not None and start >= end))
            ) or end == 0:
                # As per RFC 2616 14.35.1, a range is not satisfiable only: if
                # the first requested byte is equal to or greater than the
                # content, or when a suffix with length 0 is specified.
                # https://tools.ietf.org/html/rfc7233#section-2.1
                # A byte-range-spec is invalid if the last-byte-pos value is
                # present and less than the first-byte-pos.
                self.set_status(416)  # Range Not Satisfiable
                self.set_header("Content-Type", "text/plain")
                self.set_header("Content-Range", "bytes */%s" % (size,))
                return
            if end is not None and end > size:
                # Clients sometimes blindly use a large range to limit their
                # download size; cap the endpoint at the actual file size.
                end = size
            # Note: only return HTTP 206 if less than the entire range has been
            # requested. Not only is this semantically correct, but Chrome
            # refuses to play audio if it gets an HTTP 206 in response to
            # ``Range: bytes=0-``.
            if size != (end or size) - (start or 0):
                self.set_status(206)  # Partial Content
                self.set_header(
                    "Content-Range", tornado.httputil._get_content_range(
                        start, end, size)
                )
        else:
            start = end = None

        if start is not None and end is not None:
            content_length = end - start
        elif end is not None:
            content_length = end
        elif start is not None:
            end = size
            content_length = size - start
        else:
            end = size
            content_length = size
        self.set_header("Content-Length", content_length)

        if include_body:
            evt_loop = self.server.get_event_loop()
            content = self.get_content_nonblock(
                evt_loop, self.absolute_path, start, end)
            async for chunk in content:
                try:
                    self.write(chunk)
                    await self.flush()
                except tornado.iostream.StreamClosedError:
                    return
        else:
            assert self.request.method == "HEAD"

    def _escape_filename_to_ascii(self, basename: str) -> str:
        return basename.encode("ascii", "replace").decode()

    def _escape_filename_to_utf8(self, basename: str) -> str:
        return urllib.parse.quote(basename, encoding="utf-8")

    @classmethod
    async def get_content_nonblock(
        cls,
        evt_loop: EventLoop,
        abspath: str,
        start: Optional[int] = None,
        end: Optional[int] = None
    ) -> AsyncGenerator[bytes, None]:
        with open(abspath, "rb") as file:
            if start is not None:
                file.seek(start)
            if end is not None:
                remaining = end - (start or 0)  # type: Optional[int]
            else:
                remaining = None
            while True:
                chunk_size = 64 * 1024
                if remaining is not None and remaining < chunk_size:
                    chunk_size = remaining
                chunk = await evt_loop.run_in_thread(file.read, chunk_size)
                if chunk:
                    if remaining is not None:
                        remaining -= len(chunk)
                    yield chunk
                else:
                    if remaining is not None:
                        assert remaining == 0
                    return

    @classmethod
    def _get_cached_version(cls, abs_path: str) -> Optional[str]:
        return None


class CustomFileHandler(FileRequestHandler):
    async def get(self, path: str, include_body: bool = True) -> None:
        """
        Return files from the directory by path
        Optional request args for images -> width, height
        """
        self.path = self.parse_url_path(path)
        del path
        absolute_path = self.get_absolute_path(self.root, self.path)
        self.absolute_path = absolute_path

        file_type = mimetypes.guess_type(self.absolute_path)
        if file_type[0][:5] == "image":
            width = self.get_argument("width", None)
            height = self.get_argument("height", None)
            im = Image.open(f"{self.absolute_path}")
            buff = io.BytesIO()
            if width and height:
                im.thumbnail((int(width), int(height)), Image.ANTIALIAS)
                # pic = im.resize((int(width), int(height)))
                im.save(buff, format="JPEG", quality=100)
            else:
                im.save(buff, format="JPEG", quality=100)
            pic_bytes = buff.getvalue()
            self.modified = self.get_modified_time()
            self.set_headers()
            self.write(pic_bytes)
            im.close()
        else:
            await super().get(self.path, include_body)

# Default Handler for unregistered endpoints


class AuthorizedErrorHandler(AuthorizedRequestHandler):
    def prepare(self) -> None:
        super(AuthorizedRequestHandler, self).prepare()
        self.set_status(404)
        raise tornado.web.HTTPError(404)

    def check_xsrf_cookie(self) -> None:
        pass

    def write_error(self, status_code: int, **kwargs) -> None:
        err = {'code': status_code, 'message': self._reason}
        if 'exc_info' in kwargs:
            err['traceback'] = "\n".join(
                traceback.format_exception(*kwargs['exc_info']))
        self.finish({'error': err})


class RedirectHandler(AuthorizedRequestHandler):
    def get(self, *args, **kwargs) -> None:
        url: Optional[str] = self.get_argument('url', None)
        if url is None:
            try:
                body_args: Dict[str, Any] = json.loads(self.request.body)
            except json.JSONDecodeError:
                body_args = {}
            if 'url' not in body_args:
                raise tornado.web.HTTPError(
                    400, "No url argument provided")
            url = body_args['url']
            assert url is not None
        self.redirect(url)
