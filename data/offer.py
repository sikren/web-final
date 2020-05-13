import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Offer(SqlAlchemyBase):
    __tablename__ = 'offers'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    lon = sqlalchemy.Column(sqlalchemy.Float, nullable=False, index=True)
    lat = sqlalchemy.Column(sqlalchemy.Float, nullable=False, index=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo = sqlalchemy.Column(sqlalchemy.Binary, nullable=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
