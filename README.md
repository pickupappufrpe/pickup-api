# pickup-api
API REST da plataforma Pick-Up

URL: https://pickupbsiapi.herokuapp.com/

#### Recursos:

método | endpoint | request | obs:
------------ | ------------- | ------------- | -------------
**create_user** | /user | POST | {"username": "chandler", "password": "123456"} / retorna o id recém criado, "new_user_id"
**login** | /login | basic auth | retorna um token JWT
**get_one_user** | /user/id | GET | passar token no header 'x-access-token'
**get_all_users** | /user | GET |
**delete_user** | /user/id | DELETE | /user/1
**create_person** | /user/id/person/ | POST / | {"name":"Chandler", "surname":"Bing"}*
**create_contact** | /user/id/contact | POST | {"email": "chandler@friends.com", "phone": "55888999999"}*
**create_type** | /type | POST | {"type":"jogador"}

*com token inicial

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