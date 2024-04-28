import requests
import pytest


base_url = 'http://localhost:8000'
add_drug_url = f'{base_url}/add_drug'
get_drugs_url = f'{base_url}/get_drugs'
get_drug_by_id_url = f'{base_url}/get_drug_by_id'
update_drug_url = f'{base_url}/update_drug'
delete_drug_url = f'{base_url}/delete_drug'

new_drug = {
    "id": 99,
    "name": "Aspirin",
    "manufacturer": "Bayer",
    "expiration_date": "2025-12-31T00:00:00",
    "description": "Used to reduce pain, fever, or inflammation."
}

updated_data = {
    "id": 99,
    "name": "Aspirin",
    "manufacturer": "Bayer",
    "expiration_date": "2025-12-31T00:00:00",
    "description": "Updated description for Aspirin"
}

service_url = 'http://localhost:80/drug_labels'
search_query = 'aspirin'


def test_add_drug():
    response = requests.post(add_drug_url, json=new_drug)
    assert response.status_code == 200
    assert response.json()['name'] == "Aspirin"

def test_get_drugs():
    response = requests.get(get_drugs_url)
    assert response.status_code == 200
    drugs = response.json()
    assert any(drug['name'] == "Aspirin" for drug in drugs)

def test_get_drug_by_id():
    response = requests.get(f"{get_drug_by_id_url}?drug_id=99")
    assert response.status_code == 200
    assert response.json()['id'] == 99

def test_update_drug():
    response = requests.put(f"{update_drug_url}?drug_id=99", json=updated_data)
    assert response.status_code == 200
    assert response.json()['description'] == "Updated description for Aspirin"

def test_delete_drug():
    response = requests.delete(f"{delete_drug_url}?drug_id=99")
    assert response.status_code == 200
    assert response.json() == {"message": "Drug deleted"}

    response = requests.get(f"{get_drug_by_id_url}?drug_id=99")
    assert response.status_code == 404

# def test_get_drug_labels():
#     response = requests.get(f"{service_url}?search_query={search_query}")
#     assert response.status_code == 200
#
#     data = response.json()
#     assert 'results' in data
#     assert len(data['results']) > 0
#
#     drug_info = data['results'][0]
#     assert 'active_ingredient' in drug_info or 'inactive_ingredient' in drug_info

