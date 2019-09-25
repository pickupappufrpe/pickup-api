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
**create_contact** | /contact | POST | {"email": "chandler@friends.com", "phone": "55888999999"}* (retorna "contact_id" que foi criado)
**set_contact** | /user/id/contact | POST | {"contact_id":"1"}*
**get_contact** | /user/id/contact | GET |  **
**create_group** | /group | POST | {"group_name":"jogador"}
**set_group** | /user/id/group | POST | {"group":"jogador"}*

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