import json

from auth import hash_password
from database import UserModel, Session, AdvertisementModel
from errors import ApiError
from validate import validate, CreateUserSchema, CreateAdvertisementSchema, PatchAdvertisementSchema, PatchUserSchema
from aiohttp import web
from sqlalchemy.exc import IntegrityError


async def get_user(user_id: int, session: Session):
    user = await session.get(UserModel, user_id)
    if user is None:
        raise web.HTTPNotFound(text=json.dumps({
            'status': 'error',
            'description': 'User not found'
        }),
            content_type='application/json')
    return user


class UserView(web.View):

    @property
    def session(self):
        return self.request['session']

    async def get(self):
        user_id = int(self.request.match_info['user_id'])
        user = await get_user(user_id, self.session)

        return web.json_response({
            'id': user.id,
            'email': user.email
        })

    async def post(self):
        user_data = validate(await self.request.json(), CreateUserSchema)
        user_data['password'] = hash_password(user_data['password'])
        new_user = UserModel(**user_data)
        self.session.add(new_user)
        try:
            await self.session.commit()
        except IntegrityError:
            raise ApiError(400, 'email is busy')
        return web.json_response({
            'id': new_user.id,
            'email': new_user.email
        })

    async def patch(self):
        user_id = int(self.request.match_info['user_id'])
        user_patch = validate(await self.request.json(), PatchUserSchema)
        if 'password' in user_patch:
            user_patch['password'] = hash_password(user_patch['password'])
        user = await get_user(user_id, self.session)
        for field, value in user_patch.items():
            setattr(user, field, value)
        self.session.add(user)
        await self.session.commit()

        return web.json_response({
            'id': user.id,
            'email': user.email
        })

    async def delete(self):
        user_id = int(self.request.match_info['user_id'])
        user = await get_user(user_id, self.session)
        await self.session.delete(user)
        await self.session.commit()
        return web.json_response({
            'status': 'deleted'
        })


async def get_adv(advertisement_id: int, session: Session):
    adv = await session.get(AdvertisementModel, advertisement_id)
    if adv is None:
        raise web.HTTPNotFound(text=json.dumps({
            'status': 'error',
            'description': 'advertisement not found'
        }),
            content_type='application/json')
    return adv


class AdvertisementView(web.View):

    @property
    def session(self):
        return self.request['session']

    async def get(self):
        adv_id = int(self.request.match_info['advertisement_id'])
        adv = await get_adv(adv_id, self.session)

        return web.json_response({
            'id': adv.id,
            'description': adv.description,
            'title': adv.title,
            'created_at': adv.created_at.isoformat(),
            'user_id': adv.user_id,
             })

    async def post(self):
        advertisement_data = validate(await self.request.json(), CreateAdvertisementSchema)
        new_advertisement = AdvertisementModel(**advertisement_data)
        self.session.add(new_advertisement)
        await self.session.commit()

        return web.json_response({
                'id': new_advertisement.id,
                'title': new_advertisement.title,
                'description': new_advertisement.description,
                'user_id': new_advertisement.user_id,
            })

    async def patch(self):
        adv_id = int(self.request.match_info['advertisement_id'])
        adv_patch = validate(await self.request.json(), PatchAdvertisementSchema)
        adv = await get_adv(adv_id, self.session)
        for field, value in adv_patch.items():
            setattr(adv, field, value)
        self.session.add(adv)
        await self.session.commit()

        return web.json_response({
                'id': adv.id,
                'title': adv.title,
                'description': adv.description,
                'user_id': adv.user_id
            })

    async def delete(self):
        adv_id = int(self.request.match_info['advertisement_id'])
        adv = await get_adv(adv_id, self.session)
        await self.session.delete(adv)
        await self.session.commit()

        return web.json_response({
            'status': 'deleted'
        })
