from typing import List
from src.domain.models import Users
from src.infra.config import DBConnectionHandler
from src.infra.entities import Users as UsersModel
from src.data.interfaces import UserRepositoryInterface


class UserRepository(UserRepositoryInterface):

    @classmethod
    def insert_user(cls, name: str, password: str):

        with DBConnectionHandler() as db_connection:
            try:
                new_user = UsersModel(name=name, password=password)
                db_connection.session.add(new_user)
                db_connection.session.commit()
                return Users(id=new_user.id, name=new_user.name,
                             password=new_user.password)
            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()
        return None

    @classmethod
    def select_user(cls, user_id: int = None, name: str = None) -> List[Users]:
        try:
            query_data = None

            if user_id and not name:
                with DBConnectionHandler() as db_connection:
                    data = db_connection.session.query(UsersModel).filter_by(
                        id=user_id).one()
                    query_data = [data]

            elif not user_id and name:
                with DBConnectionHandler() as db_connection:
                    data = db_connection.session.query(UsersModel).filter_by(
                        name=name).all()
                    query_data = [data]

            elif user_id and name:
                with DBConnectionHandler() as db_connection:
                    data = db_connection.session.query(UsersModel).filter_by(
                        id=user_id, name=name).one()
                    query_data = [data]

            return query_data

        except:
            db_connection.session.rollback()
            raise
        finally:
            db_connection.session.close()

        return None
