import pytest
from datetime import datetime, timedelta
from epic_events.models.base import Base

# Separated data definitions
data = {
    "roles": [
        {"id": 1, "name": "commercial"},
        {"id": 2, "name": "support"},
        {"id": 3, "name": "management"}
    ],
    "users": [
        {
            "id": 1,
            "name": "lucas",
            "email": "manager_lucas@test.com",
            "password": "$argon2id$v=19$m=65536,t=3,p=4$9NJxw0p+9aD3SJIN7cCNfw$u+fLlgVRcqz3h6c9vt1K9rYamP6sSOLr+xJC+T5vqPY",
            "role": 3
        },
        {
            "id": 2,
            "name": "leo",
            "email": "support_leo@test.com",
            "password": "$argon2id$v=19$m=65536,t=3,p=4$9NJxw0p+9aD3SJIN7cCNfw$u+fLlgVRcqz3h6c9vt1K9rYamP6sSOLr+xJC+T5vqPY",
            "role": 2
        },
        {
            "id": 3,
            "name": "sarah",
            "email": "commercial_sarah@test.com",
            "password": "$argon2id$v=19$m=65536,t=3,p=4$9NJxw0p+9aD3SJIN7cCNfw$u+fLlgVRcqz3h6c9vt1K9rYamP6sSOLr+xJC+T5vqPY",
            "role": 1
        },
        {
            "id": 4,
            "name": "marion",
            "email": "commercial_marion@test.com",
            "password": "$argon2id$v=19$m=65536,t=3,p=4$9NJxw0p+9aD3SJIN7cCNfw$u+fLlgVRcqz3h6c9vt1K9rYamP6sSOLr+xJC+T5vqPY",
            "role": 1
        },
        {
            "id": 5,
            "name": "william",
            "email": "support_william@test.com",
            "password": "$argon2id$v=19$m=65536,t=3,p=4$9NJxw0p+9aD3SJIN7cCNfw$u+fLlgVRcqz3h6c9vt1K9rYamP6sSOLr+xJC+T5vqPY",
            "role": 2
        }
    ],
    "clients": [
        {
            "id": 1,
            "name": "client",
            "email": "client@test.com",
            "phone": "0123456789",
            "company": "shop",
            "creation_date": datetime(2023, 9, 24, 14, 30, 0),
            "update_date": datetime(2023, 9, 24, 14, 30, 0),
            "commercial_contact_id": 3
        }
    ],
    "contracts": [
        {
            "id": 1,
            "client_id": 1,
            "total_amount": 100,
            "left_to_pay": 20,
            "status": "SIGNED",
            "creation_date": datetime(2023, 9, 24, 14, 30, 0),
            "update_date": datetime(2023, 9, 24, 14, 30, 0),
        },
        {
            "id": 2,
            "client_id": 1,
            "total_amount": 100,
            "left_to_pay": 0,
            "status": "UNSIGNED",
            "creation_date": datetime(2023, 9, 24, 14, 30, 0),
            "update_date": datetime(2023, 9, 24, 14, 30, 0),
        },
    ],
    "events": [
        {
            "id": 1,
            "contract_id": 1,
            "start_date": (datetime.now() + timedelta(days=1)),
            "end_date": (datetime.now() + timedelta(days=2)),
            "support_contact_id": 2,
            "location": "Paris",
            "attendees": 20,
            "notes": "Lorem ipsum",
            "creation_date": datetime(2023, 9, 24, 14, 30, 0),
            "update_date": datetime(2023, 9, 24, 14, 30, 0),
        },
    ]
}

def prepare_sqlalchemy_mock_config():
    """Prepare mock configuration for SQLAlchemy.

    Returns:
        list: A list of tuples containing table names and their corresponding data.
    """
    return [(table, data[table]) for table in data]

@pytest.fixture(scope="function")
def sqlalchemy_declarative_base():
    """Fixture for providing the SQLAlchemy Declarative Base.

    Returns:
        Base: The SQLAlchemy Declarative Base.
    """
    return Base

@pytest.fixture(scope="function")
def sqlalchemy_mock_config():
    """Fixture for providing mock configuration for SQLAlchemy tables.

    Returns:
        list: Mock configuration data for SQLAlchemy tables.
    """
    return prepare_sqlalchemy_mock_config()
