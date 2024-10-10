# Unkey FastAPI Boilerplate

This project is a Unkey FastAPI Boilerplate to protect API routes. We have three routes:

- `api/hello` (GET): This is an unprotected route that will return just hello world
- `api/create` (GET): This will create a key using unkey and return key as well as keyid
- `api/protected` (POST): This route is protected and requires a key that you just created using create a route in the header.


## Requirements

- [Unkey](https://app.unkey.com)
- Python 3.7+
- FastAPI
- Uvicorn (for running the FastAPI app)


## Setup

1. Go to [Unkey Dashboard](https://app.unkey.com)
2. Create a new API from [apis](https://app.unkey.com/apis)
3. Go to settings/root-key and create a rootkey with the permissions `create_key` and `read_key`
4. Set up env variables `cp .env.example .env ` and then set the rootkey and the API ID we just created.
  ```bash
  UNKEY_ROOT_KEY=""
  UNKEY_API_ID=""
```




## Local Setup

**Clone the repo**

   ```bash
   git clone https://github.com/harshsbhat/unkey-fastapi-boilerplate.git
   cd unkey-fastapi-boilerplate
  ```

**Install the dependencies**

   ```bash
  pip install -r requirements.txt
  ```

**Run the project**

   ```bash
  uvicorn main:app --reload
  ```

This should start the project on port  `http://127.0.0.1:8000`

## Usage

**Unprotected Route**
   ```bash
  curl http://127.0.0.1:8000/api/hello
  ```

**Create key**

This should return the key and keyId 

   ```bash
  curl http://127.0.0.1:8000/api/create
  ```

**Protected Route**

This will verify the key using Unkey and then grant access or deny it.

   ```bash
  curl -X POST http://127.0.0.1:8000/api/protected \
  -H "Authorization: Bearer <UNKEY_ROOT_KEY>
  ```

