# Simple API

Simple API is a test task. The main aim is to develop a service using FastAPI and PostgreSQL that implements a basic role-based system, processes, and stores incoming requests, and sends messages via Telegram.

Main Features:
- Processing and storing JSON requests containing the following data: bottoken, chatid, message.
- Sending messages to Telegram, with the Telegram API response saved in the database. 
  - Role-based access control:
  - Admin: Full access to all records.
  - Manager: Access to records of their assigned users.
- User: Access to their own records only.
- PostgreSQL for data storage, including user, role, and request data, with proper relationships between tables. 
- API creation with endpoints to manage records and roles. 
- Documentation and testing of the API, including examples of requests and a database dump for testing purposes.


## Installation

Use the package manager what you prefer like **Poetry** or **PDM**, or use a virtual environment

```
python -m venv venv
```

Then activate, on a Linux or Mac machine: `source ./venv/bin/activate ` or on a Windows machine:
`.\venv\Scripts\activate.bat`. Then install dependencies
```
pip install -e .
 ```


## Usage

>Before running API you need to do a few steps:
>- you need to create at least one `.env.prod` file, 
  you can override this file with `.env` file to set the dev environment
>- run docker-compose from `app.yaml` or you can set 
  your relationship by changing 


To run API use the command or run with IDE
```
uvicorn main:app --host 0.0.0.0 --port 8000
```

You can read the documentation by `$APP_ROOT/redocs` or define your own path overwrites `APP_REDOCS_URL`. 
If you want to test api manually, it's recommended to use **Postman** with import by path`$APP_ROOT/openapi`.


## Testing

Testing is divided into two parts app tests and policy tests, respectively.  

### App tests

> Run only with your `.env`. Dataset is located by path `./sql`

To run API test use `ApiClientTest` 

### Policy tests

To test the policies, you can run the following command

```
docker run --rm --name cerbos_test -t -v ./cerbos/:/cerbos_data \
   ghcr.io/cerbos/cerbos:latest compile --tests=/cerbos_data/tests /cerbos_data/policies
```
