from faker import Faker
from .pet_repository import PetRepository
from src.infra.config import DBConnectionHandler
from src.infra.entities import Pets
from src.infra.entities.pets import AnimalTypes


faker = Faker()
pet_repository = PetRepository()
db_connection = DBConnectionHandler()


def test_insert_pet():
    name = faker.name()
    specie = "fish"
    age = faker.random_number(digits=1)
    user_id = faker.random_number()

    new_pet = pet_repository.insert_pet(name, specie, age, user_id)
    engine = db_connection.get_engine()
    query_pet = engine.execute(
        "SELECT * FROM pets WHERE id='{}';".format(new_pet.id)).fetchone()

    assert new_pet.id == query_pet.id
    assert new_pet.name == query_pet.name
    assert new_pet.specie == query_pet.specie
    assert new_pet.age == query_pet.age
    assert new_pet.user_id == query_pet.user_id

    engine.execute(f"DELETE FROM pets WHERE id='{new_pet.id}';")


def test_select_pet():
    pet_id = faker.random_number(digits=4)
    name = faker.name()
    specie = "fish"
    age = faker.random_number(digits=1)
    user_id = faker.random_number()

    specie_mock = AnimalTypes("fish")
    data = Pets(id=pet_id, name=name, specie=specie_mock,
                age=age, user_id=user_id)

    engine = db_connection.get_engine()
    engine.execute("INSERT INTO pets (id, name, specie, age, user_id) VALUES ('{}','{}','{}','{}','{}');".format(
        pet_id, name, specie, age, user_id))

    query_pets1 = pet_repository.select_pet(pet_id=pet_id)
    query_pets2 = pet_repository.select_pet(user_id=user_id)
    query_pets3 = pet_repository.select_pet(pet_id=pet_id, user_id=user_id)

    assert (query_pets1[0].id == data.id and query_pets1[0].name == data.name and query_pets1[0].specie ==
            data.specie and query_pets1[0].age == data.age and query_pets1[0].user_id == data.user_id)
    assert (query_pets2[0].id == data.id and query_pets2[0].name == data.name and query_pets2[0].specie ==
            data.specie and query_pets2[0].age == data.age and query_pets2[0].user_id == data.user_id)
    assert (query_pets3[0].id == data.id and query_pets3[0].name == data.name and query_pets3[0].specie ==
            data.specie and query_pets3[0].age == data.age and query_pets3[0].user_id == data.user_id)


    engine.execute("DELETE FROM pets WHERE id='{}';".format(pet_id))
