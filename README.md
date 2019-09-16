# pickup-api
API REST da plataforma Pick-Up

# Recursos:

método | endpoint | request | obs:
------------ | ------------- | ------------- | -------------
**create_user** | /user | POST | {"login": "jose", "password": "123456"}
**login** | /login | basic auth | retorna um token JWT
**get_one_user** | /user/id | GET | /user/1
**get_all_users** | /user | GET |
**delete_user** | /user/id | DELETE | /user/1

