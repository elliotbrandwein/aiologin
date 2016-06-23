#!/usr/bin/python3

import asyncio

from aiohttp import web
from aiohttp_session import session_middleware, SimpleCookieStorage

import aiologin


class User(aiologin.AbstractUser):
    @property
    def authenticated(self):
        return True

    @property
    def forbidden(self):
        return False


@aiologin.secured
async def handler(request):
    print(await request.aiologin.current_user())
    return web.Response(body=b'OK')


async def login(request):
    await request.aiologin.login(User())
    return web.Response()


async def logout(request):
    await request.aiologin.logout()
    return web.Response()


async def init(loop):
    app = web.Application(middlewares=[
        session_middleware(SimpleCookieStorage())
    ])

    aiologin.setup(app, User)

    app.router.add_route('GET', '/', handler)
    app.router.add_route('GET', '/login', login)
    app.router.add_route('GET', '/logout', logout)
    srv = await loop.create_server(
        app.make_handler(), '0.0.0.0', 8080)
    return srv


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
