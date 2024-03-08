import enum
from sqlalchemy import Column, Integer, String, Boolean, func, Table, Date, Enum
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime


class Base(DeclarativeBase):
    pass


class Role(enum.Enum):
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    second_name = Column(String(50), nullable=False)
    mail = Column(String(60), unique=True, nullable=False)
    birthday = Column(Date, nullable=True)
    addition = Column(String(300), nullable=True)
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now())

    user_id =  Column(Integer, ForeignKey("users.id"),nullable=True)
    user = relationship("User" , backref="contacts", lazy="joined")


note_m2m_tag = Table(
    "note_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("note_id", Integer, ForeignKey("notes.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    mail = Column(String(160), unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    created_at = Column('created_at', DateTime, default=func.now(), nullable=True)
    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now())
    role = Column("role", Enum(Role), default=Role.user) #, nullable=True


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String(150), nullable=False)
    done = Column(Boolean, default=False)
    tags = relationship("Tag", secondary=note_m2m_tag, backref="notes")
    # user_id = Column(Integer, ForeignKey("users.id",  ondelete="CASCADE"))
    # user = relationship("User", backref="notes", lazy="joined")
    created_at = Column('created_at', DateTime, default=func.now(), nullable=True)
    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now())


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True)
