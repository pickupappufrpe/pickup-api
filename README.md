# pickup-api
API REST da plataforma Pick-Up

URL: https://pickupbsiapi.herokuapp.com/

Com exceção de login e signup todas as requisições devem carregar o token no header **'x-access-token'**

#### core.py:
método | endpoint | request | obs:
------------ | ------------- | ------------- | -------------
**login** | /login?user_group=1 | GET | Basic Auth. Retorna um token JWT

#### users:
método | endpoint | request | obs:
------------ | ------------- | ------------- | -------------
**signup** | /user | POST | {"username": "chandler", "password": "123456", "name":"Chandler", "surname":"Bing", "group_id":"1"}
**get_user_by_id** | /user/<user_id> | GET | Retorna usuário com todos os atributos preenchidos.
**get_user_by_username** | /user/username/<username> | GET | Retorna usuário com todos os atributos preenchidos.
**delete_user** | /user/<user_id> | DELETE | Delete um usuário
**get_players** | /players | GET | Retorna usuários do tipo jogador.

#### addresses:
método | endpoint | request | obs:
------------ | ------------- | ------------- | -------------
**get_all_states** | /state | GET | 
**get_city_by_state** | /state/<state_id>/city | GET |

#### bookings:
método | endpoint | request | obs:
------------ | ------------- | ------------- | -------------
**add_booking** | /booking | POST | {"spot_id":"42" "day":"01/01/2020", "start_time":"20:00:00", "end_time":"21:00:00"}
**get_spot_bookings** | /spot/<spot_id>/booking | GET | **

#### photos:
método | endpoint | request | obs:
------------ | ------------- | ------------- | -------------
**upload_spot_photo** | /spot/<spot_id>/photo | POST | form-data com key **file**
**upload_user_photo** | /user/<spot_id>/photo | POST | form-data com key **file**
**get_spot_photo_list** | /spot/<spot_id>/photo/list | GET |
**get_user_photo_list** | /user/<spot_id>/photo/list | GET |
**get_photo_by_filename** | /photo/<filename> | GET |

#### schedules:
método | endpoint | request | obs:
------------ | ------------- | ------------- | -------------
**add_schedule** | /schedule | POST | {"spot_id":"42", "week_day":"4", "opening_time":"06:00:00", "closing_time":"22:00:00"}

#### spots:
método | endpoint | request | obs:
------------ | ------------- | ------------- | -------------
**create_spot** | /spot | POST | {"spot_name": "Ilha do Retiro", "ground_id":"1", "price":"50",...}
**get_my_spots** | /spot/my | GET | retorna os espaços do proprietário logado
**get_all_spots** | /spot | GET |


#### Tipos de usuário:
user_group | id |
------------ | ------------- |
jogador | 1
locador | 2
arbitro | 3

#### Tipos de terreno (ground_id):
ground | id |
------------ | ------------- |
Quadra | 1
Grama | 2
Grama Sintetica | 3
Terra | 4


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