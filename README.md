# Chat App

The following project is a chat application that allows users view and chat with other users. Users login with their id, see other users that can chat with, and chat with them by sending messages and viewing the chat history.

The app uses the following tools and frameworks:
- Django + HTMX
- Docker + docker-compose
- Postgres + pgAdmin

## Setup
In order to setup the app:
1. Clone the repo

```
git clone https://github.com/Arman-Mojaver/django-project.git
```
2. Run the following make command

```
make setup
```

The command will:
- Create a .env file
- Start db containers
- Start web container
- Run migrations
- Create seed data in the db
- Open the login page


3. After running the command, open http://localhost:8000/login/ (Already open from `make start`), and introduce an ID. The `make start` command creates 10 users (1-5 have messages with other users, 6-10 do not have messages with other users)


## Links
web: http://localhost:8000/login/

Django admin: http://localhost:8000/admin/

pgAdmin: http://localhost:8082/


## Environments
The app has 3 environments: `production`, `development`, `testing`

In order to change between environments:
- change the ENVIRONMENT variable in .env
- Recreate the containers:
```
make down && make up
```


## Tests
Tests are run with the following command:
```
make pytest
```

The command can be safely run without changing the environment in .env. The state of production and development environments will be not affected by running the tests.


## Django admin
In order to access the Django admin page, first a superuser needs to be created. Create a superuser by running the following command:
- development environment:
```
make superuser-dev
```
- production environment:
```
make superuser-prod
```

Once created, go to http://localhost:8000/admin/ and introduce the newly created superuser credentials.

## Create/Delete users
Currently, the app does not support creating/deleting users in the web UI.

### Create a user
1. Go to the Django admin page: http://localhost:8000/admin/
![Django login.png](Documentation%2FDjango%20login.png)
2. Introduce the superuser username and password (If no superuser exists go to the `Django admin` section of this README, and create a superuser)

![Django admin.png](Documentation%2FDjango%20admin.png)
3. Click on Users (under CHAT app)

![Users.png](Documentation%2FUsers.png)
4. click `ADD USER` (on the top right corner)

![Add user.png](Documentation%2FAdd%20user.png)
5. introduce fullname and email, click `SAVE`


### Delete a user
1. Go to the Django admin page: http://localhost:8000/admin/
![Django login.png](Documentation%2FDjango%20login.png)
2. Introduce the superuser username and password (If no superuser exists go to the `Django admin` section of this README, and create a superuser)

![Django admin.png](Documentation%2FDjango%20admin.png)
3. Click on Users (under CHAT app)

![Users.png](Documentation%2FUsers.png)
4. Select the user/users to be deleted.

![Users selected.png](Documentation%2FUsers%20selected.png)
5. Click con action. Click on `Delete selected users`

![Action clicked.png](Documentation%2FAction%20clicked.png)
6. Click on go.

![Click go.png](Documentation%2FClick%20go.png)
7. Click on `Yes, I'm sure`
![Confirm delete.png](Documentation%2FConfirm%20delete.png)

## pgAdmin
pgAdmin is a Web UI to manage Postgres databases. In order to access it, go to http://localhost:8082/.
When accessing it for the first time, there will be no servers nor databases available.
### Add a server and database
1. Go to http://localhost:8082/
![pgadmin main.png](Documentation%2Fpgadmin%20main.png)
2. Click on `Add New Server`

![pgadmin general modal.png](Documentation%2Fpgadmin%20general%20modal.png)
3. Add a server name (any name, but recommended that it matches the environment)

![pgadmin connections modal.png](Documentation%2Fpgadmin%20connections%20modal.png)
4. Add a given environment's parameters, click `SAVE`

![pdamin added server.png](Documentation%2Fpdamin%20added%20server.png)

The environment data is available in `django-project/config/`:
```
https://github.com/Arman-Mojaver/django-project/tree/main/config
```
