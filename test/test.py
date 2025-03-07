import set_configs
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from httpx import AsyncClient, ASGITransport
from app.main import app
from datetime import date
from app.models.ORMModels import Base, Student, Course, Enrollment
from app.Config import DB_URL

engine = create_async_engine(DB_URL)

@pytest.fixture(scope="session", autouse=True)
async def mock_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    testing_session_local = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with testing_session_local() as session:
        students = [
            Student(name="Alice", age=20, email="alice@example.com"),
            Student(name="Bob", age=22, email="bob@example.com"),
        ]
        courses = [
            Course(name="Math 101", credit=3),
            Course(name="History 101", credit=2),
        ]
        enrollments = [
            Enrollment(student_id=1, course_id=1, start_date=date(2022, 9, 1), grade=90),
            Enrollment(student_id=2, course_id=2, start_date=date(2022, 3, 12), grade=85),
        ]

        session.add_all(students + courses + enrollments)
        await session.commit()

@pytest.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_get_students(async_client):
    response = await async_client.get("/students")
    assert response.status_code == 200
    json_response = response.json()

    json_response = sorted(json_response, key=lambda obj: obj["id"])

    assert len(json_response) == 2
    assert json_response[0]["id"] == 1
    assert json_response[0]["name"] == "Alice"
    assert json_response[0]["age"] == 20
    assert json_response[0]["email"] == "alice@example.com"
    assert json_response[1]["id"] == 2
    assert json_response[1]["name"] == "Bob"
    assert json_response[1]["age"] == 22
    assert json_response[1]["email"] == "bob@example.com"

@pytest.mark.asyncio
async def test_get_student_by_id(async_client):
    response = await async_client.get("/students/1")
    assert response.status_code == 200
    json_response = response.json()

    assert json_response["id"] == 1
    assert json_response["name"] == "Alice"
    assert json_response["age"] == 20
    assert json_response["email"] == "alice@example.com"

@pytest.mark.asyncio
async def test_get_student_by_id_not_found(async_client):
    response = await async_client.get("/students/999")
    assert response.status_code == 404
    json_response = response.json()

    assert json_response == {'detail': 'Student with id student_id=999 not found.',}

@pytest.mark.asyncio
async def test_post_student(async_client):
    payload = {
        "name": "Rephael",
        "age": 28,
        "email": "rephael@gmail.com"
    }
    response = await async_client.post("/students", json=payload)

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["id"] == 3
    assert json_response["name"] == "Rephael"
    assert json_response["age"] == 28
    assert json_response["email"] == "rephael@gmail.com"

@pytest.mark.asyncio
async def test_update_student(async_client):
    payload = {
        "name": "John",
        "age": 28,
        "email": "john@gmail.com"
    }
    response = await async_client.put("/students/1", json=payload)

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["id"] == 1
    assert json_response["name"] == "John"
    assert json_response["age"] == 28
    assert json_response["email"] == "john@gmail.com"

@pytest.mark.asyncio
async def test_update_student_not_found(async_client):
    payload = {
        "name": "John",
        "age": 28,
        "email": "john@gmail.com"
    }
    response = await async_client.put("/students/999", json=payload)

    assert response.status_code == 404
    json_response = response.json()

    assert json_response == {'detail': 'Student with id student_id=999 not found.'}

@pytest.mark.asyncio
async def test_update_student_no_data(async_client):
    payload = {
        "name": None,
        "age": None,
        "email": None
    }
    response = await async_client.put("/students/999", json=payload)

    assert response.status_code == 400
    json_response = response.json()

    assert json_response == {'detail': 'No parameters provided for update.'}

@pytest.mark.asyncio
async def test_delete_student(async_client):
    response = await async_client.delete("/students/2")

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["id"] == 2
    assert json_response["name"] == "Bob"
    assert json_response["age"] == 22
    assert json_response["email"] == "bob@example.com"

@pytest.mark.asyncio
async def test_delete_student_not_found(async_client):
    response = await async_client.delete("/students/999")

    assert response.status_code == 404
    json_response = response.json()

    assert json_response == {'detail': 'Student with student_id=999 does not exist.',}
