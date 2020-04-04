# SUORA

![Video](https://github.com/muhammet-mucahit/suora/blob/master/video/suora.gif)

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have ***Python3***, ***pip*** and ***node*** installed on their local machines.

## Database Setup
You should create databases and fill them with data

```
createdb suora
psql suora < suora.psql
```

## Credential Setup
```
export POSTGRESS_HOST=localhost:5432
export POSTGRESS_DATABASE=suora
```

### Virtual Environment
```
python3 -m venv venv
. venv/bin/activate
```

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
or
```
FLASK_APP=flaskr FLASK_ENV=development flask run
```

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
createdb suora_test
psql suora_test < suora.psql 
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 


## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
- Response codes
- Messages
- Error types
### Endpoints 
- Organized by resource
- Include each endpoint
- Sample request 
- Arguments including data types
- Response object including status codes and data types 

## Authors
@muhammet-mucahit