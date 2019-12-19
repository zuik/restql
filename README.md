# restql
## Motivation

The project aims to remove the boilerplate code in writing a web application. The JavaScript library is model after the Python `sqlalchemy` library. Because of this, you could use JavaScript to interact with the database through the `sqlalchemy`-flavored API. In Python, you can create an API server by just passing in the `sqlalchemy` model.

## High-level approach

The project utilize `Flask` to create an API for the ORM calls from JS to interact with the database through Python-`sqlalchemy` layer. 

The call in JS are call to endpoints defined when the developer passes the model into the `Flask` side. 


## Project structure

### Python server
The server is needed to handle the requests from JS library and connect with `sqlalchemy` to interact with the database.

For now, please run `python model.py` in the `restql` folder to generate a sample SQLite database. Then the server can be start with `python view.py`.

### JavaScript library

The JavaScript library is modelled after `sqlalchemy`'s API. 

The JavaScript library is in the `js` folder. Please `npm install` then `npm run start`.

#### `filter` criteria

Since we can't overload operator with JS, we translate the filter criteria to a JS object.

```
User.name == "hello"
{"name": {"eq": "hello"}}

User.age <= 10
{"age": {"lte": 10}}

User.age <= 10 AND User.name == "hello"
{"&&": [
    {"name": {"eq": "hello"}},
    {"age": {"lte": 10}}
]}
```
