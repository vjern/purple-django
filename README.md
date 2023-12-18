## Endpoints

```py
```

```sh
# list users
GET /users
# create user
POST /users {name}
# add exclusion
POST /exclusions {name, name}
# list exclusions
GET /exclusions
# Draw a list of secret santas
GET /draw
# should return error if impossible because of exclusions
# Get draw history
GET /history?n=5
```