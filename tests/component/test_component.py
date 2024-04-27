import requests
import pytest


base_url = 'http://localhost:8000'
add_drug_url = f'{base_url}/add_drug'
get_drugs_url = f'{base_url}/get_drugs'
get_drug_by_id_url = f'{base_url}/get_drug_by_id'
update_drug_url = f'{base_url}/update_drug'
delete_drug_url = f'{base_url}/delete_drug'

new_drug = {
    "name": "Aspirin",
    "manufacturer": "Bayer",
    "expiration_date": "2025-12-31T00:00:00",
    "description": "Used to reduce pain, fever, or inflammation."
}


@pytest.fixture(scope="function")
def create_drug():
    response = requests.post(add_drug_url, json=new_drug)
    drug_id = response.json()['id']
    yield drug_id
    requests.delete(f"{delete_drug_url}?drug_id={drug_id}")

def test_add_drug():
    response = requests.post(add_drug_url, json=new_drug)
    assert response.status_code == 200
    assert response.json()['name'] == "Aspirin"

def test_get_drugs():
    response = requests.get(get_drugs_url)
    assert response.status_code == 200
    drugs = response.json()
    assert any(drug['name'] == "Aspirin" for drug in drugs)

def test_get_drug_by_id(create_drug):
    drug_id = create_drug
    response = requests.get(f"{get_drug_by_id_url}?drug_id={drug_id}")
    assert response.status_code == 200
    assert response.json()['id'] == drug_id

def test_update_drug(create_drug):
    drug_id = create_drug
    updated_data = {"description": "Updated description for Aspirin"}
    response = requests.put(f"{update_drug_url}?drug_id={drug_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()['description'] == "Updated description for Aspirin"

def test_delete_drug(create_drug):
    drug_id = create_drug
    response = requests.delete(f"{delete_drug_url}?drug_id={drug_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Drug deleted"}

    response = requests.get(f"{get_drug_by_id_url}?drug_id={drug_id}")
    assert response.status_code == 404
