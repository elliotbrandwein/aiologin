#!/usr/bin/python3
from aiohttp.test_utils import TestClient, loop_context, unittest_run_loop
from aiohttp import request
import asyncio
from urllib.parse import parse_qs

from aiohttp import web
from aiohttp_session import session_middleware, SimpleCookieStorage

import aiologin

print("file run")


class TestUser(aiologin.AbstractUser):

    # User classes need attributes to be identified with, in this case we use
    # email and password
    def __init__(self, email, password):
        print("user class made")
        self.email = email
        self.password = password

    # the properties of authenticated and forbidden must be overridden form the
    # parent class or else an exception will be thrown.
    @property
    def authenticated(self):
        return True

    @property
    def forbidden(self):
        return False

async def auth_by_header(request, key):
    print("inside the auth_by_header method")
    if key == '1234567890':
        return TestUser('Test@User.com', 'foobar')
    return None

async def auth_by_session(request, profile):
    print("inside the auth_by_session method")
    if 'email' in profile and profile['email'] == 'trivigy@gmail.com' and \
            'password' in profile and profile['password'] == 'blueberry':
        return TestUser(profile['email'], profile['password'])
    return None
# this method is not required by the aiologin class, however you might want to
# use a method like this to authenticate your user
async def auth_by_form(request, email, password):
    print("inside the auth_by_forum method")
    if email == 'trivigy@gmail.com' and password == 'blueberry':
        return TestUser(email, password)
    return None


@aiologin.secured
async def handler(request):
    print("inside the handler method which is the handler for the '/' route")
    # print(await request.aiologin.current_user())
    return web.Response(body=b'OK')


async def login(request):
    print("inside the login method which is the handler for the '/login' route")
    args = parse_qs(request.query_string)
    user = await auth_by_form(request, args['email'][0], args['password'][0])
    if user is None:
        raise web.HTTPUnauthorized
    # remember is false by default, but should be set at your discretion
    await request.aiologin.login(user, remember=False)
    return web.Response()


async def logout(request):
    print(
        "inside the logout method which is the handler for the '/logout' route")
    await request.aiologin.logout()
    return web.Response()


# noinspection PyShadowingNames
async def init(loop):
    print("in the init method")
    app = web.Application(middlewares=[
        session_middleware(SimpleCookieStorage())
    ])
    aiologin.setup(
        app=app,
        auth_by_header=auth_by_header,
        auth_by_session=auth_by_session
    )

    app.router.add_route('GET', '/', handler)
    app.router.add_route('GET', '/login', login)
    app.router.add_route('GET', '/logout', logout)
    srv = await loop.create_server(
        app.make_handler(), '0.0.0.0', 8080)
    print("init is done, loop has been created with all the routes")
    return srv


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
try:
    print("run forever loop is about to start, so the init is done")
    print("")
    loop.run_forever()
except KeyboardInterrupt:
    pass
