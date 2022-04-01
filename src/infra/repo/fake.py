from src.infra.config import DBConnectionHandler
from src.infra.entities import Users


class FakerRepo:
    @classmethod
    def insert(cls):
        with DBConnectionHandler() as db_connection:
            try:
                new_user = Users(name="Programador", password="password")
                db_connection.session.add(new_user)
                db_connection.session.commit()
            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()