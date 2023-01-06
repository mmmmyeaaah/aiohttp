import requests

from tests.config import API_URL


def test_root():
    response = requests.get(API_URL)
    assert response.status_code == 404


def test_get_user_by_id(create_user):
    response = requests.get(f'{API_URL}/users/{create_user["id"]}')
    assert response.status_code == 200
    assert response.json()['email'] == create_user['email']


def test_get_user_not_exist():
    response = requests.get(f'{API_URL}/users/99999')
    assert response.status_code == 404
    assert response.json() == {'status': 'error', 'description': 'User not found'}


def test_create_user():
    response = requests.post(f'{API_URL}/users/', json={'email': 'test@example.com', 'password': 'password'})
    assert response.status_code == 200
    json_data = response.json()
    assert 'id' in json_data
    assert json_data['email'] == 'test@example.com'


def test_create_user_some_email():
    response = requests.post(f'{API_URL}/users/', json={'email': 'testsss@example.com', 'password': 'password'})
    response = requests.post(f'{API_URL}/users/', json={'email': 'testsss@example.com', 'password': 'password'})
    assert response.status_code == 400
    assert response.json()['error'] == 'email is busy'


def test_create_user_without_email():
    response = requests.post(f'{API_URL}/users/', json={'password': 'password'})
    assert response.status_code == 400
    assert response.json() == {'error': [{'loc': ['email'], 'msg': 'field required', 'type': 'value_error.missing'}]}


def test_patch_user(create_user):
    response = requests.patch(f'{API_URL}/users/{create_user["id"]}', json={'email': 'new_email'})
    assert response.status_code == 200
    assert response.json()['email'] == 'new_email'

    response = requests.get(f'{API_URL}/users/{create_user["id"]}')
    assert response.status_code == 200
    assert response.json()['email'] == 'new_email'


def test_delete_user(create_user):
    response = requests.delete(f'{API_URL}/users/{create_user["id"]}')
    assert response.status_code == 200
    assert response.json() == {'status': 'deleted'}

    response = requests.get(f'{API_URL}/users/{create_user["id"]}')
    assert response.status_code == 404


def test_get_advertisement(create_advertisement):
    response = requests.get(f'{API_URL}/adv/{create_advertisement["id"]}')
    assert response.status_code == 200
    assert response.json()['description'] == create_advertisement['description']
    assert response.json()['title'] == create_advertisement['title']
    assert response.json()['created_at'] == create_advertisement['created_at']
    assert response.json()['user_id'] == create_advertisement['user_id']


def test_create_advertisement(create_user):
    response = requests.post(f'{API_URL}/adv/', auth=(create_user['email'], '1234'),
                             json={'title': 'tomato',
                                   'description': 'tasty',
                                   'user_id': create_user['id']
                                   })
    assert response.status_code == 200
    json_data = response.json()
    assert 'title' in json_data
    assert json_data['title'] == 'tomato'


def test_patch_advertisement(create_advertisement):
    response = requests.patch(f'{API_URL}/adv/{create_advertisement["id"]}',
                              auth=(create_advertisement['user_email'], '1234'),
                              json={'description': 'mmm'})
    assert response.status_code == 200
    json_data = response.json()
    assert json_data['description'] == 'mmm'


def test_delete_advertisement(create_advertisement):
    response = requests.delete(f'{API_URL}/adv/{create_advertisement["id"]}',
                               auth=(create_advertisement['user_email'], '1234'))
    assert response.status_code == 200
