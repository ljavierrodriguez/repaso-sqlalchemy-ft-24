from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, or_, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=True)
    name = Column(String(120))
    active = Column(Boolean(), default=True)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    message = Column(String(255), nullable=False)
    date = Column(DateTime())
    to_users_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    from_users_id = Column(Integer, ForeignKey('users.id'), nullable=False)


engine = create_engine('sqlite:///base_de_datos.db')


with engine.connect() as connection:
    Base.metadata.create_all(connection)


Session = sessionmaker(bind=engine)
session = Session()


# CRUD

# INSERT
"""
user1 = User(username="john.doe@gmail.com", password="123456", name="John Doe", active=True)
session.add(user1)
session.commit()

user2 = User()
user2.username = "jane.doe@gmail.com"
user2.password = "123456"
user2.name = "Jane Doe"
user2.active = True
session.add(user2)
session.commit()

msg = Message()
msg.message = "porque lo vamos a funar"
msg.to_users_id = 2
msg.from_users_id = 1
msg.date = datetime.now()
session.add(msg)
session.commit()
"""

# SELECT

# Buscar todos los usuarios
users = session.query(User).all() # []
for user in users:
    print(user.name)

# Buscar todos los mensajes
messages = session.query(Message).all() # []
for msg in messages:
    print(msg.message)
else:
    print("Listado de mensajes vacio")


# Buscar al usuario Jane Doe
user = session.query(User).filter_by(name="Jane Doe").first()
if user:
    print("Usuario encontrado")
else:
    print("Usuario no existe")

# UPDATE

# Buscar al usuario Jane Doe y cambiar el password del mismo
user = session.query(User).filter_by(name="Jane Doe").first()
if user:
    user.password = "my-password"
    session.commit()
    print("Password Actualizado")


# Buscar mensajes inapropiados:
messages = session.query(Message).filter(
    or_(
        Message.message.contains('droga'),
        Message.message.contains('funa')
    )
).all()
print("Total mensajes con palabras claves")
print(len(messages))

messages = session.query(Message).filter(func.DATE(Message.date) == '2024-04-18', Message.from_users_id==2).all()
print("Total mensajes con fecha indicada")
print(len(messages))

messages = session.query(Message).filter(func.DATE(Message.date).between('2024-04-01', '2024-04-18'), Message.from_users_id==1).all()
print("Total mensajes con fecha indicada")
print(len(messages))