import json

import sqlalchemy
from flask import Flask, request, g, jsonify, abort
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker

from utils import AlchemyEncoder

app = Flask(__name__)
app.json_encoder = AlchemyEncoder


def create_session():
    if "DB_URI" not in app.config:
        raise Exception("What is the database we are connecting to?")

    uri = app.config.get("DB_URI")
    engine = create_engine(uri, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def get_session():
    if "session" not in g:
        g.session = create_session()
        return g.session
    else:
        return g.session


def create_endpoint(model):
    table = model.__table__  # type: sqlalchemy.schema.Table
    table_name = table.name

    @app.route(f"/{table_name}")
    def select_all():
        session = get_session()
        finalize = request.args.get("finalize", "all")
        if finalize == "all":
            r = session.query(model).all()
            return jsonify(r)
        else:
            return abort(400)
    @app.route(f"/{table_name}/filter")
    def filter():
        session = get_session()
        q = session.query(model)

        filter = json.loads(request.args.get("filter"))
        print(filter)
        if filter:
            for k, v in filter.items():
                if "eq" in v.keys():
                 q = q.filter(getattr(model, k) == v["eq"])

        finalize = request.args.get("finalize", "all")
        if finalize != "all":
            return abort(400)
        else:
            return jsonify(q.all())
    return app


@app.teardown_appcontext
def shutdown_session(exception=None):
    ''' Enable Flask to automatically remove database sessions at the
     end of the request or when the application shuts down.
     Ref: http://flask.pocoo.org/docs/patterns/sqlalchemy/
    '''
    if hasattr(g, 'session'):
        g.session.close()


if __name__ == '__main__':
    from model import User

    app.config["DB_URI"] = "sqlite:///test.db"

    app = create_endpoint(User)

    app.run(debug=True)
