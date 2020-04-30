import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Tutorials(SqlAlchemyBase):
    __tablename__ = 'tutorials'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    preview = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    for_registered_users = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')