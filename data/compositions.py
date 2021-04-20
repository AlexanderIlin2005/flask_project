import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Composition(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'compositions'
    Class = sqlalchemy.Column(sqlalchemy.Integer)
    Name = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    Literature_type = sqlalchemy.Column(sqlalchemy.String)
    Year = sqlalchemy.Column(sqlalchemy.String)
    Jenre = sqlalchemy.Column(sqlalchemy.String)
    Author = sqlalchemy.Column(sqlalchemy.String)
    Author_portrait = sqlalchemy.Column(sqlalchemy.String)
    Years_of_life = sqlalchemy.Column(sqlalchemy.String)
    Painting = sqlalchemy.Column(sqlalchemy.String)
    Movie = sqlalchemy.Column(sqlalchemy.String)
    Music = sqlalchemy.Column(sqlalchemy.String)
    Reading_time = sqlalchemy.Column(sqlalchemy.String)
    Another_author_compositions = sqlalchemy.Column(sqlalchemy.String)
    Illustrations = sqlalchemy.Column(sqlalchemy.String)

    def print_name(self):
        return self.Name

    def __repr__(self):
        return f'<User>{self.Name}'
