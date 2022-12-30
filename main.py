from views import UserView, AdvertisementView
from aiohttp import web
from database import engine, Base
from middlewares import session_middleware


app = web.Application()


async def orm_context(app: web.Application):
    print('START')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    print('SHUTDOWN')

app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)
app.add_routes(
    [
        web.get('/users/{user_id:\d+}', UserView),
        web.patch('/users/{user_id:\d+}', UserView),
        web.delete('/users/{user_id:\d+}', UserView),
        web.post('/users/', UserView)
    ]
)


app.add_routes(
    [
        web.post('/adv/', AdvertisementView),
        web.get('/adv/{advertisement_id:\d+}', AdvertisementView),
        web.patch('/adv/{advertisement_id:\d+}', AdvertisementView),
        web.delete('/adv/{advertisement_id:\d+}', AdvertisementView),
    ]
)

if __name__ == '__main__':
    web.run_app(app)
