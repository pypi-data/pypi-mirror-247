import os

import dotenv

import proximal_energy

dotenv.load_dotenv()

API_KEY = os.getenv("PROXIMAL_API_KEY")


def test_create_client():
    client = proximal_energy.ProximalClient(API_KEY)
    assert client is not None


def test_get_root():
    client = proximal_energy.ProximalClient(API_KEY)
    response = client.get_root()
    assert response.status_code == 200


def test_get_projects():
    client = proximal_energy.ProximalClient(API_KEY)
    response = client.get_projects()
    assert response.status_code == 200
