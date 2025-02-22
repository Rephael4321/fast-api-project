import pytest
import os
os.environ["TESTING"] = "true"
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app
from datetime import date
from models.ORMModels import Base, Student, Course, Enrollment
from time import time
from Config import DB_URL

engine = create_engine(DB_URL)

client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def mock_db():
    Base.metadata.drop_all(bind=engine)

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(bind=engine)

    with TestingSessionLocal() as session:
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
        session.commit()

def test_get_async_test():
    start_time = time()
    response = client.get("/async_test")
    end_time = time()
    
    total_time = end_time - start_time
    assert response.status_code == 200
    json_response = response.json()

    assert json_response == {'message': 'Response after 5 seconds',}
    assert total_time > 5

def test_get_students():
    response = client.get("/students")
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

def test_get_student_by_id():
    response = client.get("/students/1")
    assert response.status_code == 200
    json_response = response.json()

    assert json_response["id"] == 1
    assert json_response["name"] == "Alice"
    assert json_response["age"] == 20
    assert json_response["email"] == "alice@example.com"

def test_get_student_by_id_not_found():
    response = client.get("/students/999")
    assert response.status_code == 404
    json_response = response.json()

    assert json_response == {'detail': 'Student with id student_id=999 not found.',}

def test_post_student():
    payload = {
        "name": "Rephael",
        "age": 28,
        "email": "rephael@gmail.com"
    }
    response = client.post("/students", json=payload)

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["id"] == 3
    assert json_response["name"] == "Rephael"
    assert json_response["age"] == 28
    assert json_response["email"] == "rephael@gmail.com"

def test_update_student():
    payload = {
        "name": "John",
        "age": 28,
        "email": "john@gmail.com"
    }
    response = client.put("/students/1", json=payload)

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["id"] == 1
    assert json_response["name"] == "John"
    assert json_response["age"] == 28
    assert json_response["email"] == "john@gmail.com"

def test_update_student_not_found():
    payload = {
        "name": "John",
        "age": 28,
        "email": "john@gmail.com"
    }
    response = client.put("/students/999", json=payload)

    assert response.status_code == 404
    json_response = response.json()

    assert json_response == {'detail': 'Student with id student_id=999 not found.'}

def test_update_student_no_data():
    payload = {
        "name": None,
        "age": None,
        "email": None
    }
    response = client.put("/students/999", json=payload)

    assert response.status_code == 400
    json_response = response.json()

    assert json_response == {'detail': 'No parameters provided for update.'}

def test_delete_student():
    response = client.delete("/students/2")

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["id"] == 2
    assert json_response["name"] == "Bob"
    assert json_response["age"] == 22
    assert json_response["email"] == "bob@example.com"

def test_delete_student_not_found():
    response = client.delete("/students/999")

    assert response.status_code == 404
    json_response = response.json()

    assert json_response == {'detail': 'Student with student_id=999 does not exist.',}
