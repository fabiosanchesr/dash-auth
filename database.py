from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
import os


url = URL.create(
    "postgresql+psycopg2",
    username=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME')
)


engine = create_engine(url, echo=True)


Session = sessionmaker(bind=engine)
session = Session()


# data = Users(username=func.lower('fabio'), password='fabio', email=func.lower('fabio@art-technologies.com.br'))
# session.add(data)
# session.commit()


# data = session.query(Users).filter_by(username=func.lower('John')).first()
# session.delete(data)
# session.commit()


# data = session.query(Users).filter_by(username=func.lower('John')).first()
# data.value = 99
# session.commit()


# data = session.query(Users).filter_by(username=func.lower('FABIO')).all()
# for item in data:
#     print(item.id, item.username, item.email)

