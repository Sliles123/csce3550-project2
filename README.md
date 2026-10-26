# CSCE 3550 Project 2: JWKS Server with SQLite

**Author:** Dylan Liles (djl0213)

A JWKS (JSON Web Key Set) server written in Python. It signs JWTs with RSA keys and publishes the matching public keys. The private keys are stored in a SQLite database, so they survive a server restart.

## What it does

- On start, it creates `totally_not_my_privateKeys.db` in the current folder with the required `keys` table.
- It stores at least one **valid** key (expires in 1 hour) and one **expired** key, as PKCS#1 PEM bytes.
- `POST /auth` signs and returns a JWT with a valid key. With `?expired=true` it signs with an expired key, so the JWT is already expired.
- `GET /.well-known/jwks.json` returns the public keys of every unexpired key in the database.
- Every other method on those paths returns `405 Method Not Allowed` with an `Allow` header. Unknown paths return `404`.
- Authentication is mocked: HTTP Basic auth and a JSON body (`{"username": "...", "password": "..."}`) are both accepted, and the username goes in the token's `sub` claim.

## SQL injection protection

Every query that takes a value uses `?` placeholders, so SQLite binds the values separately from the SQL text. Nothing is ever formatted into a query string. For example:

```python
INSERT_KEY_SQL = "INSERT INTO keys (key, exp) VALUES (?, ?)"
conn.execute(INSERT_KEY_SQL, (pem, exp))
```

The test suite includes a check that a value containing SQL (`x'); DROP TABLE keys; --`) is stored as plain data.

## Project layout

```
main.py                  Entry point: python main.py
jwks_server/
    config.py            Port, database file name, key lifetime
    database.py          SQLite access (parameterized queries only)
    keys.py              RSA key generation, PEM (de)serialization, JWK conversion
    tokens.py            JWT signing
    server.py            HTTP handler and server startup
tests/                   pytest suite (100% coverage)
requirements.txt         Runtime dependencies
requirements-dev.txt     Test and lint dependencies
```

## Setup (Windows PowerShell)

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

## Run the server

```powershell
python main.py
```

The server listens on `http://127.0.0.1:8080`. Press Ctrl+C to stop it.

## Run the tests

```powershell
pytest
```

Coverage is reported automatically. The run fails if coverage drops below 80%.

## Lint

```powershell
flake8
```

No output means no issues.

## Gradebot

With the server running, in a second terminal opened in this folder:

```powershell
.\gradebot.exe project2 --port 8080 --code-dir jwks_server --database totally_not_my_privateKeys.db
```

## Screenshots

### Gradebot output

![Gradebot output](screenshots/gradebot.png)

### Test suite and coverage

![Test coverage](screenshots/tests.png)
