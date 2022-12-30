import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from auth import hash_password
from database import Base, UserModel, AdvertisementModel
from pytest import fixture


engine = create_engine('postgresql://vic:1234@127.0.0.1:5434/db_aiohttp')
Session = sessionmaker(bind=engine)


@fixture(scope='session', autouse=True)
def prepare_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@fixture()
def create_user():
    with Session() as session:
        new_user = UserModel(
            email=f'user{time.time()}@mail.ru',
            password=hash_password('1234')
        )
        session.add(new_user)
        session.commit()
        return {
            'id': new_user.id,
            'email': new_user.email,
        }


@fixture()
def create_advertisement():
    with Session() as session:
        new_user = UserModel(
            email=f'user{time.time()}@mail.ru',
            password=hash_password('1234')
        )
        session.add(new_user)
        session.commit()
        new_advertisement = AdvertisementModel(
            title='new advertisement',
            description='descr',
            user_id=new_user.id
        )
        session.add(new_advertisement)
        session.commit()
        return {
            'id': new_advertisement.id,
            'title': new_advertisement.title,
            'description': new_advertisement.description,
            'user_id': new_advertisement.user_id,
            'user_email': new_user.email,
            'created_at': new_advertisement.created_at.isoformat()
        }
