import sqlalchemy
from sqlalchemy import create_engine
from models_BD import create_tables, USERS, APPLICANTS, FAVORITES
from key_BD import username, password, name_bd

engine = create_engine(f'postgresql+psycopg2://{username}:{password}@localhost:5432/{name_bd}')

create_tables(engine)
print(create_tables(engine))