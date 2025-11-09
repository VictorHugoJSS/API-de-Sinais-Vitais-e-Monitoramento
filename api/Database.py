from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
import os

postgres_username = os.getenv("POSTGRES_USERNAME")
postgres_pw = os.getenv("POSTGRES_PW")
postgres_db = os.getenv("POSTGRES_DATABASE")
postgres_host = os.getenv("POSTGRES_H")

engine = create_engine(f"postgres://{postgres_username}:{postgres_pw}@{postgres_host}/{postgres_db}")
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

def init_db():
    metadata.create_all(bind=engine)
    