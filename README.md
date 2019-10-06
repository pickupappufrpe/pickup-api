# pickup-api
API REST da plataforma Pick-Up

URL: https://pickupbsiapi.herokuapp.com/

#### Recursos:

método | endpoint | request | obs:
------------ | ------------- | ------------- | -------------
**create_user** | /user | POST | {"username": "chandler", "password": "123456"} / retorna o id recém criado, "new_user_id"
**login** | /login | GET | basic auth / retorna um token JWT
**get_one_user** | /user/id | GET | **
**get_all_users** | /user | GET | **
**delete_user** | /user/id | DELETE | /user/1
**create_person** | /person | POST | {"name":"Chandler", "surname":"Bing"}* (retorna "person_id" que foi criado)*
**set_person** | /user/id/person | POST | {"person_id":"1"}*
**get_person** | /user/id/person | GET | **
**get_all_persons** | /person | GET | **
**create_contact** | /contact | POST | {"email": "chandler@friends.com", "phone": "55888999999"}* (retorna "contact_id" que foi criado)
**set_contact** | /user/id/contact | POST | {"contact_id":"1"}*
**get_contact** | /user/id/contact | GET |  **
**create_group** | /group | POST | {"group_name":"jogador"}
**get_all_groups** | /group | GET | **
**set_group** | /user/id/group | POST | {"group":"jogador"}*
**create_address** | /address | POST | {"street":"Baker", "number":"221", "neighborhood":"Marylebone"}**
**set_address** | /spot/id/address | POST | {"address_id":"1"}**
**get_address** | /spot/id/address | GET | **
**create_spot** | /spot | POST | {"spot_name": "Ilha do Retiro"}**
**set_spot_contact** | /spot/id/contact | POST | {"group":"jogador"}**
**create_state** | /state | POST | {"state_name":"Pernambuco"}**
**create_city** | /city | POST | {"city_name":"Recife"}**
**set_state** | /city/id/state | POST | {"state_name":"Bahia"}**
**set_city** | /address/id/city | POST | {"city_id":"5"}**
**get_city** | /city/id | GET | **
**get_state** | /state/id | GET | **
**get_all_cities** | /city | GET | **
**get_all_states** | /state | GET | **

Passar token no header 'x-access-token'

*com token inicial

**com token de usuário logado

#### Gerando o banco de dados:

```
$ python
>>> from core import db
>>> db.create_all()
```

#### Executando os testes unitários:

```
python -m unittest -v tests
```