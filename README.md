## Endpoints

```py
```

```sh
# list users
GET /users
# create user
POST /users {name}
# add ban entry
POST /bans {name, name}
# list ban entries
GET /bans
# Draw a list of secret santas
GET /draw
# should return error if impossible because of bans
# Get draw history
GET /history?n=5
```