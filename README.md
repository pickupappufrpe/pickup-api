# pickup-api
API REST da plataforma Pick-Up

URL: https://pickupbsiapi.herokuapp.com/

#### Recursos:

método | endpoint | request | obs:
------------ | ------------- | ------------- | -------------
**create_user** | /user | POST | {"login": "jose", "password": "123456"}
**login** | /login | basic auth | retorna um token JWT
**get_one_user** | /user/id | GET | passar token no header 'x-access-token'
**get_all_users** | /user | GET |
**delete_user** | /user/id | DELETE | /user/1

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