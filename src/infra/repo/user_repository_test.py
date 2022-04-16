from faker import Faker
from src.infra.config import DBConnectionHandler
from .user_repository import UserRepository
from src.infra.entities import Users as UsersModel

faker = Faker()
user_repository = UserRepository()
db_connection = DBConnectionHandler()


def test_insert_user():
    name = faker.name()
    password = faker.password()
    engine = db_connection.get_engine()

    new_user = user_repository.insert_user(name, password)
    query = engine.execute(f"SELECT * FROM users WHERE id={new_user.id}"
                           ).fetchone()
    engine.execute(f"DELETE FROM users WHERE id={new_user.id}")

    assert new_user.id == query.id
    assert new_user.name == query.name
    assert new_user.password == query.password


def test_select_user():
    user_id = faker.random_number(digits=5)
    name = faker.name()
    password = faker.word()
    data = UsersModel(id=user_id, name=name, password=password)

    engine = db_connection.get_engine()
    engine.execute(
        f"INSERT INTO users (id, name, password) VALUES ('{user_id}','{name}','{password}')")
    query_user1 = user_repository.select_user(user_id=user_id)
    # query_user2 = user_repository.select_user(name=name)
    query_user3 = user_repository.select_user(user_id=user_id, name=name)

    # print(f"aqui fi {query_user2}")
    assert (data.id == query_user1[0].id and data.name ==
            query_user1[0].name and data.password == query_user1[0].password)
    # assert (data.id == query_user2[0].id and data.name ==
    #         query_user2[0].name and data.password == query_user2[0].password)
    assert (data.id == query_user3[0].id and data.name ==
            query_user3[0].name and data.password == query_user3[0].password)

    engine.execute(f"DELETE FROM users WHERE id={user_id}")
